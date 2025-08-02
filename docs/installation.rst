Installation Guide
==================

Prerequisites
-------------
- Python 3.12+
- Poetry package manager
- Pygame dependencies (SDL libraries)

Installation Steps
------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/your-username/pygame-base.git
      cd pygame-base

2. Install dependencies with Poetry:

   .. code-block:: bash

      poetry install

3. Run the game:

   .. code-block:: bash

      poetry run python -m app.main

Development Setup
-----------------
For development, install additional tools:

.. code-block:: bash

   poetry install --with dev

This installs:

- Black code formatter
- Flake8 linter
- Pytest test runner


Security Practices
==================
When using Docker for deployment:

- Verify image integrity using SHA256 digests:

  .. code-block:: bash

     docker pull ubuntu:24.04@sha256:4a0e8da5d57aeb17b0e58d1d0c5e2d6a0b0f5e1e2a3b4c5d6e7f8a9b0c1d2e3

- Runtime constraints (set in docker-compose.yml):
  - Memory limit: 512MB
  - CPU limit: 2 cores

- Security scanning is enforced through CI/CD:
  - Automatic vulnerability scans on every commit
  - Critical/high severity vulnerabilities block deployment