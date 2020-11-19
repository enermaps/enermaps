#!/bin/sh
FAILED=0
for cm in *; do
	if [ -d "${cm}" ]; then
		echo "Linting CM ${cm}"
		(cd "${cm}" && \
		black --diff --check . && \
		bandit -r . && \
		isort --check --diff . && \
		flake8 .)
		if [ $? -ne 0 ]; then
			FAILED=2
			echo "FAILED"
		fi

	fi
done
exit "${FAILED}"
