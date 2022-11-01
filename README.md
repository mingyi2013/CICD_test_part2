# Introduction to CI/CD with GitHub Actions (part II) - SBI workshop \[2022/11/01\]

This repository hosts the code used during the workshop held on 2022/11/01 at the Bioinformatics Center at UiO.

The workshop is organized in two parts:
1. In the first part we familiarized with the syntax and core features of GitHub actions.
2. In the second part we will see how concepts from 1. can be applied to write a CI/CD pipeline for a Python application.

See [robomics/2022-sbi-ci-workshop-pt1](https://github.com/robomics/2022-sbi-ci-workshop-pt1) for part I of the workshop.

## Repository layout
This repository hosts a simple Python3 package called `cryptonite`.

Note: code hosted in this repository is not related in any way to the cryptonite blockchain.

Cryptonite is a small library and CLI application for encrypting/decrypting ASCII text using [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher).

The CLI interface consists of two subcommands:
  - `cryptonite encrypt` reads plain text from stdin and writes the encrypted text to stdout. 
    The encryption key can be specified using the `--key` parameter or through the `CRYPTONITE_KEY` env variable.
  - `cryptonite decrypt` can be used to decrypt messages encrypted with `cryptonite encrypt`.
     CLI options are identical to those for `cryptonite encrypt`.

### Cryptonite usage (Python API)

```python3
from cryptonite.encrypt import encrypt
from cryptonite.decrypt import decrypt

plain_message = "abc123"

encrypted_message = encrypt(plain_message, offset=1)
decrypted_message = decrypt(encrypted_message, offset=1)

print(f"{plain_message} -> {encrypted_message} -> {decrypted_message}")
# stdout:
# abc123 -> bcd234 -> abc123
```

### Cryptonite usage (CLI)

```bash
echo "abc123" | cryptonite encrypt --key=1 | cryptonite decrypt --key=1

# stdout:
# abc123
```

## GitHub Actions CI/CD workflows

Inside folder `.github/workflows/` there are 3 workflows:
- `ci.yml` - Continuous integration workflow to build and test Cryptonite using different operative systems Python versions. 
- `cd.yml` - Continuous delivery workflow to publish Cryptonite on test.pypi and prepare artifacts for a GitHub release.
- `build-docker-image.yml` - Continuous delivery workflow to build, test and publish Cryptonite's Docker image.

The rest of the workflows are [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows),
a special kind of workflows that can be triggered from other workflows.

Example: the `make-package.yml` and `run-*-tests.yml` workflows are called by `ci.yml`.

## Exercise guidelines

There are no exercises for this session, but feel free to clone, fork or use this repo as template if you prefer to follow along the examples using your laptop.

Before running the [CD workflow](https://github.com/robomics/2022-sbi-ci-workshop-pt2/blob/main/.github/workflows/cd.yml) make sure to do the following steps (otherwise the workflow will fail):
- Open an account on [test.pypi](https://test.pypi.org/) and [create an API token](https://test.pypi.org/help/#apitoken).
- Add the following secrets to your GitHub repository ([docs](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)):
    - `TESTPIPY_USERNAME` with value `__token__`
    - `TESTPIPY_PASSWORD` with value equal to the test.pypi API token created in the previous step (including the `pypi-` prefix)
- Edit the `pyproject.toml` and replace all instances of `2022-sbi-ci-workflow-cryptonite` with e.g. `2022-sbi-ci-workflow-cryptonite-myusername`.

Head over to the [release page](https://github.com/robomics/2022-sbi-ci-workshop-pt2/releases/tag/v0.0.2) on GitHub
or to the package on [test.pypi](https://test.pypi.org/project/2022-sbi-ci-workflow-cryptonite/)
to see the result produced by a successful run of the [CD workflow](https://github.com/robomics/2022-sbi-ci-workshop-pt2/blob/main/.github/workflows/cd.yml).

#### Closing notes:

- The [CD workflow](https://github.com/robomics/2022-sbi-ci-workshop-pt2/blob/main/.github/workflows/cd.yml) can be triggered by publishing a release on GitHub.
- In this case the [release description](https://github.com/robomics/2022-sbi-ci-workshop-pt2/releases/tag/v0.0.2) was generated manually
- The entire process of creating a release, as well as uploading release assets can be automated by modifying/extending the [CD workflow](https://github.com/robomics/2022-sbi-ci-workshop-pt2/blob/main/.github/workflows/cd.yml).
