
# Make you first run:
# chmod +x setup_hooks.sh

# Then execute script by doing:
# ./setup_hooks.sh

#!/bin/bash

# Copy pre-commit hook
cp .github/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Copy post-commit hook
cp .github/hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit

echo "Git hooks have been set up."
