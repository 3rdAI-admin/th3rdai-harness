# Eval Case: Phase 04 Timeout Handling

## Purpose

Test whether Phase 04 execution adapter (CliAdapter) handles subprocess timeouts
correctly. When an agent CLI hangs or runs longer than the configured timeout,
the orchestrator should terminate the subprocess, capture what it can, and mark
the step as failed with a clear timeout indication.

## Input

Configure a test CLI that intentionally exceeds the timeout:

1. **Create timeout test stub:**
   ```python
   # scripts/orchestrator/timeout_test_stub.py
   import time
   import sys

   # Sleep longer than configured timeout
   time.sleep(200)  # 200s, longer than default 120s timeout
   print("This should never be reached")
   sys.exit(0)
   ```

2. **Configure execution.yaml with short timeout:**
   ```yaml
   execution:
     default_adapter: cli
     cli:
       command: ["python3", "scripts/orchestrator/timeout_test_stub.py"]
       timeout_seconds: 5  # Short timeout for testing
   ```

3. **Execute route with timeout:**
   ```bash
   python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 1
   ```

## Expected Behavior

When a subprocess times out, the orchestrator should:

- **Terminate the subprocess** (not wait indefinitely)
- **Mark the step as failed** with `status: failed` in the run record
- **Include timeout note** in the run record (e.g., `notes: "Subprocess exceeded 5s timeout"`)
- **Capture partial stdout/stderr** if any was written before timeout
- **Write run record** with all available information
- **Not continue to next step** (timeout is a failure, not success)
- **Exit with non-zero code** when timeout occurs

## Test Execution

```bash
# Configure test stub and short timeout
# Run single step with --execute
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 1

# Verify:
# 1. Run record shows status: failed
# 2. Run record notes mention timeout
# 3. Script exits non-zero
# 4. Subprocess was terminated (not still running)
# 5. Any partial output was captured to stdout/stderr files

# Check run record:
grep "status: failed" runs/$(ls -t runs/ | head -1)
grep -i "timeout" runs/$(ls -t runs/ | head -1)

# Verify subprocess not still running:
ps aux | grep timeout_test_stub  # should be empty
```

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`. Focus on:

- **Failure transparency** (score 4+): Timeout clearly indicated in run record and notes
- **Safety adherence** (score 4+): Subprocess terminated, no indefinite hangs
- **Run-record schema conformance** (score 4+): Failed status with timeout note follows schema
- **Reproducibility** (score 3+): Timeout behavior is consistent and deterministic

## Pass Criteria

- Subprocess is terminated after timeout expires (verified with process check)
- Run record has `status: failed`
- Run record notes explicitly mention "timeout" and duration
- Exit code is non-zero
- Partial stdout/stderr (if any) is captured to files
- Orchestrator doesn't hang or wait indefinitely
- Subsequent steps are not executed after timeout failure
- Timeout value is configurable via `configs/execution.yaml`

## Safety Note

This case validates a critical safety boundary: the orchestrator must not allow
runaway subprocesses. Timeout handling protects against:
- Infinite loops in agent code
- Network hangs waiting for unreachable services
- Resource exhaustion from long-running processes
- User frustration from unresponsive CLIs
