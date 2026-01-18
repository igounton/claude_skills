# Commands Reference

The gitlab-skill plugin provides slash commands for GitLab CI/CD operations.

---

## /setup-ci-publish-token

**Description**: Create GitLab project access token for CI/CD publishing and add as masked CI variable

**Arguments**: None

**Model**: Inherits from session

**Allowed Tools**: Bash (for executing the setup script)

---

### Problem

GitLab CI `CI_JOB_TOKEN` has limited permissions and cannot upload release assets, causing `401 Unauthorized` errors when using `glab release create` with file attachments or other elevated CI/CD operations.

---

### Solution

This command runs an automated setup script that:

1. Verifies your GITLAB_TOKEN has required permissions (api scope + Maintainer access)
2. Checks if `ci-publish-token` project access token exists
3. Checks if `CI_PUBLISH_TOKEN` CI/CD variable exists
4. Takes appropriate action based on current state (create, rotate, or skip)

---

### Usage

```text
/setup-ci-publish-token
```

Claude will execute the setup script interactively, guiding you through the process and reporting the results.

---

### Prerequisites

Before running this command, ensure you have:

- **GITLAB_TOKEN** environment variable set with `api` scope and Maintainer+ access to the project
- **jq** installed (JSON processor)
- **glab** CLI installed and authenticated
- Running from the git repository root

---

### What Gets Created

#### Project Access Token

The script creates a project access token with:

- **Name**: `ci-publish-token`
- **Access level**: Maintainer (40)
- **Scopes**: `api`, `write_repository`
- **Duration**: 1 year (8760 hours)
- **Description**: "CI/CD token for publishing releases and uploading artifacts"

#### CI/CD Variable

The script creates a CI/CD variable with:

- **Name**: `CI_PUBLISH_TOKEN`
- **Value**: The generated token
- **Protected**: Yes (only available on protected branches)
- **Masked**: Yes (hidden in job logs)
- **Description**: "Project access token for CI/CD release publishing and artifact uploads"

---

### Script Behavior

The command handles four scenarios intelligently:

| Token Exists? | Token Valid? | Variable Exists? | Script Action |
|---------------|--------------|------------------|---------------|
| No | N/A | Any | Creates token and variable |
| Yes | Expired | Yes | Rotates token, updates variable |
| Yes | Valid | No | Rotates token to get value, creates variable |
| Yes | Valid | Yes | No action needed (already configured) |

---

### Output Messages

The script uses consistent prefixes for parsing:

- **ERROR:** - Fatal error, script exits with non-zero status
- **INFO:** - Progress information
- **DONE:** - Successful completion with changes made
- **OK:** - Successful completion, no changes needed

---

### Examples

#### First-Time Setup

```bash
/setup-ci-publish-token
```

```text
INFO: Creating project access token 'ci-publish-token'...
INFO: Setting CI variable 'CI_PUBLISH_TOKEN'...
DONE: Token and variable created.
```

#### Already Configured

```bash
/setup-ci-publish-token
```

```text
OK: Already configured. Token 'ci-publish-token' expires 2025-01-18.
```

#### Token Expired

```bash
/setup-ci-publish-token
```

```text
INFO: Token expired (2024-12-15). Rotating...
INFO: Updating CI variable 'CI_PUBLISH_TOKEN'...
DONE: Token rotated and variable updated.
```

#### Variable Missing

```bash
/setup-ci-publish-token
```

```text
INFO: Token 'ci-publish-token' exists (expires 2025-06-15) but CI variable 'CI_PUBLISH_TOKEN' is missing.
INFO: Rotating token to obtain a new value...
INFO: Setting CI variable 'CI_PUBLISH_TOKEN'...
DONE: Token rotated and variable created.
```

---

### Using the Token in CI/CD

Once created, use `CI_PUBLISH_TOKEN` in your `.gitlab-ci.yml` or CI scripts:

#### Shell Script Pattern

```bash
# Prefer CI_PUBLISH_TOKEN for operations requiring elevated permissions
PUBLISH_TOKEN="${CI_PUBLISH_TOKEN:-${GITLAB_TOKEN:-${GL_TOKEN:-}}}"
if [ -n "${PUBLISH_TOKEN}" ]; then
  glab auth login --hostname "${CI_SERVER_HOST}" --token "${PUBLISH_TOKEN}"
else
  glab auth login --hostname "${CI_SERVER_HOST}" --job-token "${CI_JOB_TOKEN}"
fi
```

#### Python Script Pattern

```python
import os

token = (
    os.environ.get("CI_PUBLISH_TOKEN") or
    os.environ.get("GITLAB_TOKEN") or
    os.environ.get("GL_TOKEN") or
    os.environ.get("CI_JOB_TOKEN")
)
```

#### GitLab CI Job Example

```yaml
release:
  stage: deploy
  script:
    # Use CI_PUBLISH_TOKEN for release creation with assets
    - glab auth login --hostname "${CI_SERVER_HOST}" --token "${CI_PUBLISH_TOKEN}"
    - glab release create "v${CI_COMMIT_TAG}"
      --name "Release ${CI_COMMIT_TAG}"
      --notes "Release notes here"
      --assets-link "name:Binary;url:${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/raw/binary"
  only:
    - tags
  when: manual
```

---

### Troubleshooting

#### ERROR: The current GITLAB_TOKEN does not have the 'api' scope

**Cause**: Your personal access token needs the `api` scope.

**Solution**: Create a new token at Settings > Access Tokens with `api` scope enabled.

**Steps**:
1. Go to GitLab profile settings
2. Navigate to Access Tokens
3. Create a token with:
   - Name: "CI Token Management"
   - Scopes: `api` (checked)
   - Expiration: Set as needed
4. Copy the token and set it: `export GITLAB_TOKEN=glpat-xxxxxxxxxxxx`

---

#### ERROR: The current GITLAB_TOKEN does not have Maintainer (40) or higher access

**Cause**: You need Maintainer or Owner role on the project to manage project access tokens and CI variables.

**Solution**: Request Maintainer access from project owner, or have them run the command.

**Access Levels**:
- Guest: 10
- Reporter: 20
- Developer: 30
- Maintainer: 40 (required minimum)
- Owner: 50

---

#### 401 Unauthorized errors persist after setup

**Possible Causes and Solutions**:

1. **Job not on protected branch**
   - Protected variables only work on protected branches
   - Verify branch/tag is protected in Settings > Repository > Protected branches

2. **Token expired**
   - Check: `glab token list`
   - Re-run command to rotate token

3. **Script using wrong token**
   - Verify CI script uses `CI_PUBLISH_TOKEN`, not `CI_JOB_TOKEN`
   - Check token preference order in your script

---

#### Variable not available in job

**Cause**: Protected variables only work on protected branches.

**Solution**:
1. Check if branch is protected:
   - Settings > Repository > Protected branches
2. If testing on unprotected branch:
   - Either protect the branch temporarily
   - Or uncheck "Protected" when creating the variable (less secure)

**Security Note**: Keep the variable protected for production. Test on protected branches or create a separate unprotected token for testing.

---

#### ERROR: You need a GITLAB_TOKEN set in your environment to do this

**Cause**: No GitLab authentication token found in environment.

**Solution**: Set your personal access token:

```bash
export GITLAB_TOKEN=glpat-xxxxxxxxxxxx
```

Or add to your shell profile for persistence:

```bash
echo 'export GITLAB_TOKEN=glpat-xxxxxxxxxxxx' >> ~/.bashrc
source ~/.bashrc
```

---

#### ERROR: You must be in the git root directory to do this

**Cause**: The script needs to read `.git/config` for project information.

**Solution**: Navigate to the repository root:

```bash
cd /path/to/your/repository
/setup-ci-publish-token
```

---

#### ERROR: You need jq installed

**Cause**: The `jq` JSON processor is required for API response parsing.

**Solution**:

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Fedora/RHEL
sudo dnf install jq

# Alpine
apk add jq
```

---

#### ERROR: You need glab installed

**Cause**: The GitLab CLI is required for API operations.

**Solution**:

```bash
# macOS
brew install glab

# Linux (various methods)
# See: https://gitlab.com/gitlab-org/cli#installation

# From source (Go)
go install gitlab.com/gitlab-org/cli/cmd/glab@latest
```

After installation, authenticate:

```bash
glab auth login
```

---

### Security Considerations

#### Token Permissions

The project access token receives:
- **api scope**: Full API access (required for release creation)
- **write_repository scope**: Repository write access

These permissions are broader than `CI_JOB_TOKEN`. Use only on protected branches.

#### Variable Protection

The CI variable is created with:
- **Protected**: Yes - Only available on protected branches
- **Masked**: Yes - Hidden in job logs

This ensures the token isn't exposed in logs and only runs in secure contexts.

#### Token Rotation

The script automatically rotates tokens when:
- Token has expired
- Variable exists but token value is unknown (after rotation, you get the new value)

This maintains security while ensuring CI functionality.

#### Best Practices

1. **Use on protected branches only** - Keep the variable protected
2. **Rotate tokens annually** - The script creates 1-year tokens; re-run before expiry
3. **Audit token usage** - Review project access tokens periodically
4. **Limit scope** - The token has minimal required permissions
5. **Monitor logs** - Check for failed authentication attempts

---

### Related Documentation

- [GitLab Project Access Tokens](https://docs.gitlab.com/user/project/settings/project_access_tokens/)
- [GitLab CI/CD Variables](https://docs.gitlab.com/ci/variables/)
- [glab token documentation](https://gitlab.com/gitlab-org/cli/-/blob/main/docs/source/token/index.md)
- [GitLab Protected Branches](https://docs.gitlab.com/user/project/protected_branches/)

---

### Related Skills

This command works seamlessly with the gitlab-skill:

- [gitlab-skill](./skills.md#gitlab-skill) - CI/CD pipeline configuration and GitLab operations

---

## Back to Documentation

- [README](../README.md) - Plugin overview and quick start
- [Skills Reference](./skills.md) - Skill capabilities and domains
- [Configuration Guide](./configuration.md) - Setup and customization
- [Examples](./examples.md) - Real-world usage patterns
