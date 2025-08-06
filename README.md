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