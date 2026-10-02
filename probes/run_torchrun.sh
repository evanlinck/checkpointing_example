#!/bin/bash
# P7e/P7f/P7g: launch two copies of probe.py with torchrun, as a DDP recipe would.
# probe.py does no distributed work; each copy just logs signals with its RANK.
echo "WRAPPER torch $(python3 -c 'import torch; print(torch.__version__)' 2>/dev/null); torchrun --shutdown-timeout supported: $(torchrun --help 2>&1 | grep -q -- '--shutdown-timeout' && echo yes || echo no); TORCH_ELASTIC_SHUTDOWN_TIMEOUT=${TORCH_ELASTIC_SHUTDOWN_TIMEOUT:-unset}"
echo "WRAPPER run_torchrun.sh pid=$$ about to exec torchrun"
exec torchrun --standalone --nproc_per_node=2 probe.py "$@"
