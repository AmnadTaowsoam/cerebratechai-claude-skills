---
name: Web3 Integration
description: Enabling decentralized applications to interact with blockchain networks using Web3.js, Ethers.js, provider setup, wallet connections, and smart contract interactions.
---

# Web3 Integration

> **Current Level:** Advanced  
> **Domain:** Blockchain / Web3

---

## Overview

Web3 enables decentralized applications to interact with blockchain networks. This guide covers Web3.js, Ethers.js, provider setup, and blockchain interactions for building decentralized applications that interact with Ethereum and other blockchain networks.

---

---

## Core Concepts

### Web3 Concepts

```
Traditional Web (Web2):
Client → Server → Database

Web3:
Client → Blockchain Node → Blockchain Network
```

**Key Concepts:**
- **Provider**: Connection to blockchain node
- **Signer**: Account that can sign transactions
- **Contract**: Smart contract instance
- **Transaction**: State-changing operation
- **Gas**: Computational cost

## Web3.js vs Ethers.js

| Feature | Web3.js | Ethers.js |
|---------|---------|-----------|
| Size | ~500KB | ~88KB |
| API | Callback-based | Promise-based |
| TypeScript | Limited | Excellent |
| Documentation | Good | Excellent |
| Community | Larger | Growing |

**Recommendation**: Use **Ethers.js** for new projects.

## Provider Setup

### Infura

```typescript
// lib/web3-provider.ts
import { ethers } from 'ethers';

export class Web3Provider {
  private provider: ethers.providers.Provider;

  constructor() {
    // Infura provider
    this.provider = new ethers.providers.InfuraProvider(
      'mainnet',
      process.env.NEXT_PUBLIC_INFURA_KEY
    );
  }

  getProvider(): ethers.providers.Provider {
    return this.provider;
  }

  async getBlockNumber(): Promise<number> {
    return this.provider.getBlockNumber();
  }

  async getGasPrice(): Promise<ethers.BigNumber> {
    return this.provider.getGasPrice();
  }
}
```

### Alchemy

```typescript
// lib/alchemy-provider.ts
import { ethers } from 'ethers';

export function createAlchemyProvider(network: string = 'mainnet') {
  return new ethers.providers.AlchemyProvider(
    network,
    process.env.NEXT_PUBLIC_ALCHEMY_KEY
  );
}

// With WebSocket for real-time updates
export function createAlchemyWebSocketProvider() {
  return new ethers.providers.AlchemyWebSocketProvider(
    'mainnet',
    process.env.NEXT_PUBLIC_ALCHEMY_KEY
  );
}
```

### Multiple Providers (Fallback)

```typescript
// lib/fallback-provider.ts
export function createFallbackProvider() {
  const providers = [
    new ethers.providers.InfuraProvider('mainnet', process.env.INFURA_KEY),
    new ethers.providers.AlchemyProvider('mainnet', process.env.ALCHEMY_KEY),
    new ethers.providers.EtherscanProvider('mainnet', process.env.ETHERSCAN_KEY)
  ];

  return new ethers.providers.FallbackProvider(providers);
}
```

## Reading Blockchain Data

```typescript
// services/blockchain-reader.service.ts
import { ethers } from 'ethers';

export class BlockchainReaderService {
  constructor(private provider: ethers.providers.Provider) {}

  async getBalance(address: string): Promise<string> {
    const balance = await this.provider.getBalance(address);
    return ethers.utils.formatEther(balance);
  }

  async getTransaction(txHash: string): Promise<ethers.providers.TransactionResponse> {
    const tx = await this.provider.getTransaction(txHash);
    if (!tx) throw new Error('Transaction not found');
    return tx;
  }

  async getTransactionReceipt(txHash: string): Promise<ethers.providers.TransactionReceipt> {
    const receipt = await this.provider.getTransactionReceipt(txHash);
    if (!receipt) throw new Error('Receipt not found');
    return receipt;
  }

  async getBlock(blockNumber: number): Promise<ethers.providers.Block> {
    return this.provider.getBlock(blockNumber);
  }

  async getCode(address: string): Promise<string> {
    return this.provider.getCode(address);
  }

  async isContract(address: string): Promise<boolean> {
    const code = await this.getCode(address);
    return code !== '0x';
  }

  async getTransactionCount(address: string): Promise<number> {
    return this.provider.getTransactionCount(address);
  }

  async estimateGas(transaction: ethers.providers.TransactionRequest): Promise<ethers.BigNumber> {
    return this.provider.estimateGas(transaction);
  }
}
```

## Transactions

```typescript
// services/transaction.service.ts
export class TransactionService {
  constructor(
    private provider: ethers.providers.Provider,
    private signer: ethers.Signer
  ) {}

  async sendEther(to: string, amount: string): Promise<ethers.providers.TransactionResponse> {
    const tx = await this.signer.sendTransaction({
      to,
      value: ethers.utils.parseEther(amount)
    });

    return tx;
  }

  async sendTransaction(
    to: string,
    data: string,
    value?: string
  ): Promise<ethers.providers.TransactionResponse> {
    const tx = await this.signer.sendTransaction({
      to,
      data,
      value: value ? ethers.utils.parseEther(value) : undefined
    });

    return tx;
  }

  async waitForTransaction(
    txHash: string,
    confirmations: number = 1
  ): Promise<ethers.providers.TransactionReceipt> {
    const receipt = await this.provider.waitForTransaction(txHash, confirmations);
    return receipt;
  }

  async getTransactionStatus(txHash: string): Promise<TransactionStatus> {
    const receipt = await this.provider.getTransactionReceipt(txHash);

    if (!receipt) {
      return { status: 'pending', receipt: null };
    }

    return {
      status: receipt.status === 1 ? 'success' : 'failed',
      receipt
    };
  }
}

interface TransactionStatus {
  status: 'pending' | 'success' | 'failed';
  receipt: ethers.providers.TransactionReceipt | null;
}
```

## Gas Estimation

```typescript
// services/gas-estimation.service.ts
export class GasEstimationService {
  constructor(private provider: ethers.providers.Provider) {}

  async estimateGas(transaction: ethers.providers.TransactionRequest): Promise<GasEstimate> {
    const [gasLimit, gasPrice, feeData] = await Promise.all([
      this.provider.estimateGas(transaction),
      this.provider.getGasPrice(),
      this.provider.getFeeData()
    ]);

    // EIP-1559 (if supported)
    const maxFeePerGas = feeData.maxFeePerGas || gasPrice;
    const maxPriorityFeePerGas = feeData.maxPriorityFeePerGas || ethers.BigNumber.from(0);

    const estimatedCost = gasLimit.mul(maxFeePerGas);

    return {
      gasLimit: gasLimit.toString(),
      gasPrice: ethers.utils.formatUnits(gasPrice, 'gwei'),
      maxFeePerGas: ethers.utils.formatUnits(maxFeePerGas, 'gwei'),
      maxPriorityFeePerGas: ethers.utils.formatUnits(maxPriorityFeePerGas, 'gwei'),
      estimatedCost: ethers.utils.formatEther(estimatedCost),
      estimatedCostUSD: await this.convertToUSD(estimatedCost)
    };
  }

  async getOptimalGasPrice(): Promise<OptimalGasPrice> {
    const feeData = await this.provider.getFeeData();

    return {
      slow: feeData.gasPrice?.mul(80).div(100), // 80% of current
      standard: feeData.gasPrice,
      fast: feeData.gasPrice?.mul(120).div(100) // 120% of current
    };
  }

  private async convertToUSD(ethAmount: ethers.BigNumber): Promise<string> {
    // Get ETH price from oracle or API
    const ethPrice = await this.getETHPrice();
    const ethValue = parseFloat(ethers.utils.formatEther(ethAmount));
    return (ethValue * ethPrice).toFixed(2);
  }

  private async getETHPrice(): Promise<number> {
    // Implementation: fetch from CoinGecko, Chainlink, etc.
    return 2000; // Placeholder
  }
}

interface GasEstimate {
  gasLimit: string;
  gasPrice: string;
  maxFeePerGas: string;
  maxPriorityFeePerGas: string;
  estimatedCost: string;
  estimatedCostUSD: string;
}

interface OptimalGasPrice {
  slow?: ethers.BigNumber;
  standard?: ethers.BigNumber;
  fast?: ethers.BigNumber;
}
```

## Event Listening

```typescript
// services/event-listener.service.ts
export class EventListenerService {
  constructor(private provider: ethers.providers.Provider) {}

  listenToBlocks(callback: (blockNumber: number) => void): () => void {
    this.provider.on('block', callback);

    // Return cleanup function
    return () => {
      this.provider.off('block', callback);
    };
  }

  listenToPendingTransactions(callback: (txHash: string) => void): () => void {
    this.provider.on('pending', callback);

    return () => {
      this.provider.off('pending', callback);
    };
  }

  async listenToContractEvents(
    contract: ethers.Contract,
    eventName: string,
    callback: (...args: any[]) => void
  ): Promise<() => void> {
    contract.on(eventName, callback);

    return () => {
      contract.off(eventName, callback);
    };
  }

  async getHistoricalEvents(
    contract: ethers.Contract,
    eventName: string,
    fromBlock: number,
    toBlock: number | 'latest' = 'latest'
  ): Promise<ethers.Event[]> {
    const filter = contract.filters[eventName]();
    return contract.queryFilter(filter, fromBlock, toBlock);
  }
}

// Usage in React
function useBlockListener() {
  const [blockNumber, setBlockNumber] = useState<number>(0);

  useEffect(() => {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const listener = new EventListenerService(provider);

    const cleanup = listener.listenToBlocks((block) => {
      setBlockNumber(block);
    });

    return cleanup;
  }, []);

  return blockNumber;
}
```

## Multi-chain Support

```typescript
// lib/multi-chain.ts
export enum ChainId {
  ETHEREUM_MAINNET = 1,
  ETHEREUM_GOERLI = 5,
  POLYGON_MAINNET = 137,
  POLYGON_MUMBAI = 80001,
  BSC_MAINNET = 56,
  ARBITRUM_ONE = 42161
}

export interface ChainConfig {
  chainId: number;
  name: string;
  rpcUrl: string;
  blockExplorer: string;
  nativeCurrency: {
    name: string;
    symbol: string;
    decimals: number;
  };
}

export const CHAIN_CONFIGS: Record<ChainId, ChainConfig> = {
  [ChainId.ETHEREUM_MAINNET]: {
    chainId: 1,
    name: 'Ethereum Mainnet',
    rpcUrl: `https://mainnet.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_KEY}`,
    blockExplorer: 'https://etherscan.io',
    nativeCurrency: {
      name: 'Ether',
      symbol: 'ETH',
      decimals: 18
    }
  },
  [ChainId.POLYGON_MAINNET]: {
    chainId: 137,
    name: 'Polygon Mainnet',
    rpcUrl: 'https://polygon-rpc.com',
    blockExplorer: 'https://polygonscan.com',
    nativeCurrency: {
      name: 'MATIC',
      symbol: 'MATIC',
      decimals: 18
    }
  }
  // Add more chains...
};

export class MultiChainProvider {
  private providers: Map<ChainId, ethers.providers.Provider> = new Map();

  getProvider(chainId: ChainId): ethers.providers.Provider {
    if (!this.providers.has(chainId)) {
      const config = CHAIN_CONFIGS[chainId];
      const provider = new ethers.providers.JsonRpcProvider(config.rpcUrl);
      this.providers.set(chainId, provider);
    }

    return this.providers.get(chainId)!;
  }

  async switchChain(chainId: ChainId): Promise<void> {
    const config = CHAIN_CONFIGS[chainId];

    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: `0x${chainId.toString(16)}` }]
      });
    } catch (error: any) {
      // Chain not added, add it
      if (error.code === 4902) {
        await this.addChain(config);
      } else {
        throw error;
      }
    }
  }

  private async addChain(config: ChainConfig): Promise<void> {
    await window.ethereum.request({
      method: 'wallet_addEthereumChain',
      params: [{
        chainId: `0x${config.chainId.toString(16)}`,
        chainName: config.name,
        rpcUrls: [config.rpcUrl],
        blockExplorerUrls: [config.blockExplorer],
        nativeCurrency: config.nativeCurrency
      }]
    });
  }
}
```

## Testing

### Hardhat

```typescript
// hardhat.config.ts
import { HardhatUserConfig } from 'hardhat/config';
import '@nomicfoundation/hardhat-toolbox';

const config: HardhatUserConfig = {
  solidity: '0.8.19',
  networks: {
    hardhat: {
      chainId: 1337
    },
    goerli: {
      url: `https://goerli.infura.io/v3/${process.env.INFURA_KEY}`,
      accounts: [process.env.PRIVATE_KEY!]
    }
  }
};

export default config;

// test/integration.test.ts
import { ethers } from 'hardhat';
import { expect } from 'chai';

describe('Web3 Integration', () => {
  it('should read balance', async () => {
    const [signer] = await ethers.getSigners();
    const balance = await signer.getBalance();
    expect(balance.gt(0)).to.be.true;
  });

  it('should send transaction', async () => {
    const [sender, receiver] = await ethers.getSigners();
    
    const tx = await sender.sendTransaction({
      to: receiver.address,
      value: ethers.utils.parseEther('1.0')
    });

    await tx.wait();

    const balance = await receiver.getBalance();
    expect(balance.gte(ethers.utils.parseEther('1.0'))).to.be.true;
  });
});
```

## Error Handling

```typescript
// utils/web3-errors.ts
export class Web3ErrorHandler {
  static handle(error: any): string {
    if (error.code === 4001) {
      return 'User rejected the transaction';
    }

    if (error.code === -32603) {
      return 'Internal JSON-RPC error';
    }

    if (error.code === 'INSUFFICIENT_FUNDS') {
      return 'Insufficient funds for transaction';
    }

    if (error.code === 'UNPREDICTABLE_GAS_LIMIT') {
      return 'Cannot estimate gas; transaction may fail';
    }

    if (error.code === 'NETWORK_ERROR') {
      return 'Network connection error';
    }

    return error.message || 'Unknown error occurred';
  }

  static isUserRejection(error: any): boolean {
    return error.code === 4001;
  }

  static isInsufficientFunds(error: any): boolean {
    return error.code === 'INSUFFICIENT_FUNDS';
  }
}
```

## Security Considerations

1. **Private Keys** - Never expose private keys
2. **Input Validation** - Validate all addresses and amounts
3. **Gas Limits** - Set reasonable gas limits
4. **Nonce Management** - Handle nonce properly
5. **Rate Limiting** - Limit RPC calls
6. **Error Handling** - Handle all errors gracefully
7. **HTTPS** - Use HTTPS for RPC endpoints
8. **Provider Trust** - Use trusted providers
9. **Transaction Verification** - Verify transaction data
10. **Monitoring** - Monitor for suspicious activity

## Best Practices

1. **Use Ethers.js** - Prefer Ethers.js over Web3.js
2. **Provider Fallback** - Use multiple providers
3. **Event Listening** - Use WebSocket for real-time updates
4. **Gas Estimation** - Always estimate gas before sending
5. **Transaction Confirmation** - Wait for confirmations
6. **Error Handling** - Handle all error cases
7. **TypeScript** - Use TypeScript for type safety
8. **Testing** - Test with local blockchain
9. **Caching** - Cache blockchain data when possible
10. **Documentation** - Document all Web3 interactions
```

---

## Quick Start

### Ethers.js Setup

```javascript
import { ethers } from 'ethers'

// Connect to provider
const provider = new ethers.providers.JsonRpcProvider(
  'https://mainnet.infura.io/v3/YOUR_PROJECT_ID'
)

// Connect wallet
const wallet = new ethers.Wallet(PRIVATE_KEY, provider)

// Interact with contract
const contract = new ethers.Contract(
  CONTRACT_ADDRESS,
  ABI,
  wallet
)

// Call contract function
const result = await contract.getBalance()
```

### Web3.js Setup

```javascript
import Web3 from 'web3'

const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_PROJECT_ID')

// Get balance
const balance = await web3.eth.getBalance(ADDRESS)

// Send transaction
const tx = await web3.eth.sendTransaction({
  from: FROM_ADDRESS,
  to: TO_ADDRESS,
  value: web3.utils.toWei('1', 'ether')
})
```

---

## Production Checklist

- [ ] **Provider**: Use reliable blockchain provider (Infura, Alchemy)
- [ ] **Wallet Security**: Secure private key storage
- [ ] **Gas Estimation**: Always estimate gas before transactions
- [ ] **Error Handling**: Handle all Web3 errors gracefully
- [ ] **Transaction Confirmation**: Wait for transaction confirmations
- [ ] **Nonce Management**: Proper nonce handling
- [ ] **Rate Limiting**: Limit RPC calls to prevent throttling
- [ ] **Monitoring**: Monitor transaction status and failures
- [ ] **Testing**: Test with testnets before mainnet
- [ ] **Security**: Never expose private keys
- [ ] **Fallback**: Multiple provider fallbacks
- [ ] **Documentation**: Document all blockchain interactions

---

## Anti-patterns

### ❌ Don't: Expose Private Keys

```javascript
// ❌ Bad - Private key in code
const wallet = new ethers.Wallet('0x1234...', provider)  // Exposed!
```

```javascript
// ✅ Good - Environment variable
const wallet = new ethers.Wallet(
  process.env.PRIVATE_KEY,  // From secrets manager
  provider
)
```

### ❌ Don't: No Gas Estimation

```javascript
// ❌ Bad - Fixed gas
await contract.function({ gasLimit: 100000 })  // Might fail!
```

```javascript
// ✅ Good - Estimate gas
const gasEstimate = await contract.estimateGas.function()
await contract.function({ gasLimit: gasEstimate.mul(120).div(100) })
```

### ❌ Don't: No Error Handling

```javascript
// ❌ Bad - No error handling
const tx = await contract.function()
```

```javascript
// ✅ Good - Handle errors
try {
  const tx = await contract.function()
  await tx.wait()  // Wait for confirmation
} catch (error) {
  if (error.code === 'INSUFFICIENT_FUNDS') {
    // Handle insufficient funds
  } else {
    // Handle other errors
  }
}
```

---

## Integration Points

- **Wallet Connection** (`35-blockchain-web3/wallet-connection/`) - Wallet integration
- **Smart Contracts** (`35-blockchain-web3/smart-contracts/`) - Contract interaction
- **Secrets Management** (`24-security-practices/secrets-management/`) - Secure keys

---

## Further Reading

- [Ethers.js Documentation](https://docs.ethers.io/)
- [Web3.js Documentation](https://web3js.readthedocs.io/)
- [Ethereum Developer Resources](https://ethereum.org/en/developers/)

## Resources

- [Ethers.js Documentation](https://docs.ethers.org/)
- [Web3.js Documentation](https://web3js.readthedocs.io/)
- [Infura](https://infura.io/)
- [Alchemy](https://www.alchemy.com/)
- [Hardhat](https://hardhat.org/)
