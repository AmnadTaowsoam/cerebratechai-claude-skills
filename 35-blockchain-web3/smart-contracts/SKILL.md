---
name: Smart Contracts Integration
description: Developing and integrating smart contracts (self-executing programs on blockchain) using Solidity, contract deployment, interaction patterns, and frontend integration.
---

# Smart Contracts Integration

> **Current Level:** Advanced  
> **Domain:** Blockchain / Web3

---

## Overview

Smart contracts are self-executing programs on the blockchain. This guide covers Solidity basics, contract deployment, interaction, and frontend integration for building decentralized applications with automated, trustless execution.

---

## Smart Contract Basics

```solidity
// contracts/SimpleStorage.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleStorage {
    uint256 private value;
    
    event ValueChanged(uint256 newValue, address changedBy);
    
    function setValue(uint256 _value) public {
        value = _value;
        emit ValueChanged(_value, msg.sender);
    }
    
    function getValue() public view returns (uint256) {
        return value;
    }
}
```

## Contract ABI

```typescript
// ABI (Application Binary Interface)
const SimpleStorageABI = [
  {
    "inputs": [{ "internalType": "uint256", "name": "_value", "type": "uint256" }],
    "name": "setValue",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getValue",
    "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "anonymous": false,
    "inputs": [
      { "indexed": false, "internalType": "uint256", "name": "newValue", "type": "uint256" },
      { "indexed": false, "internalType": "address", "name": "changedBy", "type": "address" }
    ],
    "name": "ValueChanged",
    "type": "event"
  }
];
```

## Deploying Contracts

### Hardhat Deployment

```typescript
// scripts/deploy.ts
import { ethers } from 'hardhat';

async function main() {
  const SimpleStorage = await ethers.getContractFactory('SimpleStorage');
  const simpleStorage = await SimpleStorage.deploy();
  
  await simpleStorage.deployed();
  
  console.log('SimpleStorage deployed to:', simpleStorage.address);
  
  // Verify on Etherscan
  if (network.name !== 'hardhat') {
    await simpleStorage.deployTransaction.wait(6);
    await verify(simpleStorage.address, []);
  }
}

async function verify(contractAddress: string, args: any[]) {
  try {
    await run('verify:verify', {
      address: contractAddress,
      constructorArguments: args
    });
  } catch (error: any) {
    if (error.message.toLowerCase().includes('already verified')) {
      console.log('Already verified!');
    } else {
      console.error(error);
    }
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

## Interacting with Contracts

### Read Functions

```typescript
// services/contract-reader.service.ts
import { ethers } from 'ethers';

export class ContractReaderService {
  private contract: ethers.Contract;

  constructor(
    contractAddress: string,
    abi: any[],
    provider: ethers.providers.Provider
  ) {
    this.contract = new ethers.Contract(contractAddress, abi, provider);
  }

  async getValue(): Promise<number> {
    const value = await this.contract.getValue();
    return value.toNumber();
  }

  async getMultipleValues(): Promise<any> {
    // Batch multiple calls
    const [value1, value2, value3] = await Promise.all([
      this.contract.getValue(),
      this.contract.getOwner(),
      this.contract.getTotalSupply()
    ]);

    return { value1, value2, value3 };
  }

  async callStaticFunction(functionName: string, ...args: any[]): Promise<any> {
    return this.contract.callStatic[functionName](...args);
  }
}
```

### Write Functions

```typescript
// services/contract-writer.service.ts
export class ContractWriterService {
  private contract: ethers.Contract;

  constructor(
    contractAddress: string,
    abi: any[],
    signer: ethers.Signer
  ) {
    this.contract = new ethers.Contract(contractAddress, abi, signer);
  }

  async setValue(value: number): Promise<ethers.ContractTransaction> {
    const tx = await this.contract.setValue(value);
    return tx;
  }

  async setValueAndWait(value: number): Promise<ethers.ContractReceipt> {
    const tx = await this.contract.setValue(value);
    const receipt = await tx.wait();
    return receipt;
  }

  async setValueWithGasEstimate(value: number): Promise<ethers.ContractTransaction> {
    const gasEstimate = await this.contract.estimateGas.setValue(value);
    const gasLimit = gasEstimate.mul(120).div(100); // Add 20% buffer

    const tx = await this.contract.setValue(value, {
      gasLimit
    });

    return tx;
  }

  async setValueWithCustomGas(
    value: number,
    maxFeePerGas: ethers.BigNumber,
    maxPriorityFeePerGas: ethers.BigNumber
  ): Promise<ethers.ContractTransaction> {
    const tx = await this.contract.setValue(value, {
      maxFeePerGas,
      maxPriorityFeePerGas
    });

    return tx;
  }
}
```

## Contract Events

```typescript
// services/contract-events.service.ts
export class ContractEventsService {
  private contract: ethers.Contract;

  constructor(
    contractAddress: string,
    abi: any[],
    provider: ethers.providers.Provider
  ) {
    this.contract = new ethers.Contract(contractAddress, abi, provider);
  }

  listenToValueChanged(callback: (newValue: number, changedBy: string) => void): () => void {
    const listener = (newValue: ethers.BigNumber, changedBy: string) => {
      callback(newValue.toNumber(), changedBy);
    };

    this.contract.on('ValueChanged', listener);

    // Return cleanup function
    return () => {
      this.contract.off('ValueChanged', listener);
    };
  }

  async getHistoricalEvents(
    eventName: string,
    fromBlock: number,
    toBlock: number | 'latest' = 'latest'
  ): Promise<ethers.Event[]> {
    const filter = this.contract.filters[eventName]();
    return this.contract.queryFilter(filter, fromBlock, toBlock);
  }

  async getValueChangedHistory(): Promise<ValueChangedEvent[]> {
    const events = await this.getHistoricalEvents('ValueChanged', 0);

    return events.map(event => ({
      newValue: event.args!.newValue.toNumber(),
      changedBy: event.args!.changedBy,
      blockNumber: event.blockNumber,
      transactionHash: event.transactionHash
    }));
  }
}

interface ValueChangedEvent {
  newValue: number;
  changedBy: string;
  blockNumber: number;
  transactionHash: string;
}

// React hook
function useContractEvent(
  contract: ethers.Contract,
  eventName: string,
  callback: (...args: any[]) => void
) {
  useEffect(() => {
    contract.on(eventName, callback);

    return () => {
      contract.off(eventName, callback);
    };
  }, [contract, eventName, callback]);
}
```

## TypeScript Typing with TypeChain

```bash
# Install TypeChain
npm install --save-dev typechain @typechain/ethers-v5 @typechain/hardhat

# Generate types
npx hardhat typechain
```

```typescript
// hardhat.config.ts
import '@typechain/hardhat';

const config: HardhatUserConfig = {
  typechain: {
    outDir: 'typechain-types',
    target: 'ethers-v5'
  }
};

// Usage with generated types
import { SimpleStorage } from '../typechain-types';

async function useTypedContract() {
  const contract: SimpleStorage = SimpleStorage__factory.connect(
    contractAddress,
    signer
  );

  // Fully typed!
  const value: BigNumber = await contract.getValue();
  const tx: ContractTransaction = await contract.setValue(42);
}
```

## Testing Contracts

```typescript
// test/SimpleStorage.test.ts
import { expect } from 'chai';
import { ethers } from 'hardhat';
import { SimpleStorage } from '../typechain-types';

describe('SimpleStorage', () => {
  let simpleStorage: SimpleStorage;
  let owner: SignerWithAddress;
  let addr1: SignerWithAddress;

  beforeEach(async () => {
    [owner, addr1] = await ethers.getSigners();

    const SimpleStorageFactory = await ethers.getContractFactory('SimpleStorage');
    simpleStorage = await SimpleStorageFactory.deploy();
    await simpleStorage.deployed();
  });

  describe('setValue', () => {
    it('should set value correctly', async () => {
      await simpleStorage.setValue(42);
      expect(await simpleStorage.getValue()).to.equal(42);
    });

    it('should emit ValueChanged event', async () => {
      await expect(simpleStorage.setValue(42))
        .to.emit(simpleStorage, 'ValueChanged')
        .withArgs(42, owner.address);
    });

    it('should allow multiple updates', async () => {
      await simpleStorage.setValue(10);
      await simpleStorage.setValue(20);
      expect(await simpleStorage.getValue()).to.equal(20);
    });
  });

  describe('getValue', () => {
    it('should return initial value of 0', async () => {
      expect(await simpleStorage.getValue()).to.equal(0);
    });

    it('should return updated value', async () => {
      await simpleStorage.setValue(100);
      expect(await simpleStorage.getValue()).to.equal(100);
    });
  });
});
```

## Upgradeability Patterns

### Transparent Proxy

```solidity
// contracts/upgradeable/StorageV1.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract StorageV1 is Initializable, OwnableUpgradeable {
    uint256 private value;

    function initialize() public initializer {
        __Ownable_init();
    }

    function setValue(uint256 _value) public onlyOwner {
        value = _value;
    }

    function getValue() public view returns (uint256) {
        return value;
    }
}

// contracts/upgradeable/StorageV2.sol
contract StorageV2 is StorageV1 {
    uint256 private multiplier;

    function setMultiplier(uint256 _multiplier) public onlyOwner {
        multiplier = _multiplier;
    }

    function getValueWithMultiplier() public view returns (uint256) {
        return getValue() * multiplier;
    }
}
```

```typescript
// scripts/deploy-upgradeable.ts
import { ethers, upgrades } from 'hardhat';

async function main() {
  // Deploy V1
  const StorageV1 = await ethers.getContractFactory('StorageV1');
  const proxy = await upgrades.deployProxy(StorageV1, [], {
    initializer: 'initialize'
  });
  await proxy.deployed();

  console.log('Proxy deployed to:', proxy.address);

  // Upgrade to V2
  const StorageV2 = await ethers.getContractFactory('StorageV2');
  const upgraded = await upgrades.upgradeProxy(proxy.address, StorageV2);

  console.log('Upgraded to V2');
}
```

## Gas Optimization

```solidity
// Gas optimization techniques
contract GasOptimized {
    // Use uint256 instead of smaller types (except in structs)
    uint256 public value; // Good
    uint8 public smallValue; // Avoid unless in struct

    // Pack variables in structs
    struct User {
        uint128 balance;
        uint128 lastUpdate;
        address wallet; // Packed together
    }

    // Use calldata for read-only arrays
    function processData(uint256[] calldata data) external {
        // More gas efficient than memory
    }

    // Cache array length
    function sumArray(uint256[] memory arr) public pure returns (uint256) {
        uint256 total = 0;
        uint256 length = arr.length; // Cache length
        for (uint256 i = 0; i < length; i++) {
            total += arr[i];
        }
        return total;
    }

    // Use unchecked for safe operations
    function increment(uint256 x) public pure returns (uint256) {
        unchecked {
            return x + 1; // Save gas if overflow impossible
        }
    }
}
```

## Frontend Integration

```typescript
// hooks/useContract.ts
import { useMemo } from 'react';
import { useProvider, useSigner } from 'wagmi';
import { ethers } from 'ethers';

export function useContract(
  address: string,
  abi: any[]
) {
  const provider = useProvider();
  const { data: signer } = useSigner();

  const contract = useMemo(() => {
    if (signer) {
      return new ethers.Contract(address, abi, signer);
    }
    return new ethers.Contract(address, abi, provider);
  }, [address, abi, signer, provider]);

  return contract;
}

// components/ContractInteraction.tsx
function ContractInteraction() {
  const contract = useContract(CONTRACT_ADDRESS, ABI);
  const [value, setValue] = useState<number>(0);
  const [loading, setLoading] = useState(false);

  const fetchValue = async () => {
    const val = await contract.getValue();
    setValue(val.toNumber());
  };

  const updateValue = async (newValue: number) => {
    setLoading(true);
    try {
      const tx = await contract.setValue(newValue);
      await tx.wait();
      await fetchValue();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchValue();
  }, []);

  return (
    <div>
      <p>Current Value: {value}</p>
      <button onClick={() => updateValue(42)} disabled={loading}>
        {loading ? 'Updating...' : 'Set Value to 42'}
      </button>
    </div>
  );
}
```

---

## Quick Start

### Basic Smart Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleStorage {
    uint256 private value;
    
    event ValueChanged(uint256 newValue, address changedBy);
    
    function setValue(uint256 _value) public {
        value = _value;
        emit ValueChanged(_value, msg.sender);
    }
    
    function getValue() public view returns (uint256) {
        return value;
    }
}
```

### Deploy Contract

```javascript
const { ethers } = require('ethers')

const provider = new ethers.providers.JsonRpcProvider(RPC_URL)
const wallet = new ethers.Wallet(PRIVATE_KEY, provider)

// Compile contract
const contractFactory = new ethers.ContractFactory(
  abi,
  bytecode,
  wallet
)

// Deploy
const contract = await contractFactory.deploy()
await contract.deployed()

console.log('Contract deployed at:', contract.address)
```

---

## Production Checklist

- [ ] **Solidity Version**: Use latest stable Solidity version
- [ ] **Security Audit**: Audit contracts before mainnet deployment
- [ ] **Gas Optimization**: Optimize for gas efficiency
- [ ] **Testing**: Comprehensive test coverage
- [ ] **Upgradeability**: Consider upgradeable contracts if needed
- [ ] **Access Control**: Implement proper access control
- [ ] **Error Handling**: Handle errors gracefully
- [ ] **Events**: Emit events for off-chain tracking
- [ ] **Documentation**: Document contract functions
- [ ] **Verification**: Verify contract source code on Etherscan
- [ ] **Monitoring**: Monitor contract interactions
- [ ] **Backup**: Have backup deployment addresses

---

## Anti-patterns

### ❌ Don't: No Access Control

```solidity
// ❌ Bad - Anyone can call
function withdraw() public {
  payable(msg.sender).transfer(address(this).balance)
}
```

```solidity
// ✅ Good - Access control
address public owner;

modifier onlyOwner() {
  require(msg.sender == owner, "Not owner");
  _;
}

function withdraw() public onlyOwner {
  payable(owner).transfer(address(this).balance)
}
```

### ❌ Don't: Reentrancy Vulnerability

```solidity
// ❌ Bad - Reentrancy risk
function withdraw() public {
  payable(msg.sender).transfer(balances[msg.sender])
  balances[msg.sender] = 0  // Too late!
}
```

```solidity
// ✅ Good - Checks-Effects-Interactions pattern
function withdraw() public {
  uint256 amount = balances[msg.sender]
  balances[msg.sender] = 0  // Update state first
  payable(msg.sender).transfer(amount)  // Then interact
}
```

---

## Integration Points

- **Web3 Integration** (`35-blockchain-web3/web3-integration/`) - Contract interaction
- **Wallet Connection** (`35-blockchain-web3/wallet-connection/`) - User wallets
- **Secure Coding** (`24-security-practices/secure-coding/`) - Security practices

---

## Further Reading

- [Solidity Documentation](https://docs.soliditylang.org/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Smart Contract Security](https://consensys.github.io/smart-contract-best-practices/)
5. **Upgradeability** - Consider upgrade patterns
6. **Events** - Emit events for important actions
7. **Access Control** - Implement proper permissions
8. **Reentrancy Guards** - Protect against reentrancy
9. **Input Validation** - Validate all inputs
10. **Documentation** - Document all functions

## Resources

- [Solidity Documentation](https://docs.soliditylang.org/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Hardhat](https://hardhat.org/)
- [TypeChain](https://github.com/dethcrypto/TypeChain)
- [Ethers.js](https://docs.ethers.org/)
