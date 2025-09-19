# RA7 Governance Protocol

RA7's governance is managed by a Decentralized Autonomous Organization (DAO) that evolves over four phases.

## Phase 1: Foundation (Current)

*   **Platform**: Ethereum Sepolia Testnet.
*   **Voters**: 100 initial members.
*   **Voting Method**: Simple Majority.
*   **Scope**: Approving code merges and initial fund allocation.

## Multi-Sig Kill Switch

A critical safety feature is the 3-of-5 multi-signature kill switch.

*   **Keyholders**: 1 CVO, 1 DAO, 3 Randomly Selected Nodes.
*   **Action**: Can execute a network-wide halt via MQTT command `ra7/commands/AGI_HALT`.

## Contribution Workflow

1.  **Fork** the repository.
2.  Create a new branch for your feature.
3.  Write code and corresponding tests.
4.  Submit a **Pull Request** to the `main` branch.
5.  The PR will be debated and voted on by the DAO. A simple majority is required for a merge.

## RA7 Premium App

The repository includes a desktop application located in `premium_app.py` with the following features:

* Account creation and login with credentials stored using AES-256 encryption.
* Optional license key to unlock premium note lengths and features.
* Dark and light themes with a simple note-taking interface.
* Remote update checker that notifies the user when a new release is available.
* Local analytics tracking daily usage and revenue, plus referral code generation at registration.

Run the app with:

```bash
python premium_app.py
```

Dependencies are listed in `requirements.txt`. Install them with `pip install -r requirements.txt`.

### Development

After installing dependencies, verify code style and run the test suite:

```bash
python -m flake8 kill_switch.py ra7_lightlang_writer.py ra7_m2m.py birth_ritual.py eternal_clause.py cq_validator.py premium_app.py analytics.py update_checker.py test_analytics.py test_security.py
pytest -q
```
