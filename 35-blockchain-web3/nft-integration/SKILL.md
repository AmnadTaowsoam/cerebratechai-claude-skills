---
name: NFT Integration
description: Integrating Non-Fungible Tokens (NFTs) as unique digital assets on blockchain using ERC-721, ERC-1155 standards, minting, metadata management, and marketplace integration.
---

# NFT Integration

> **Current Level:** Advanced  
> **Domain:** Blockchain / Web3

---

## Overview

NFTs (Non-Fungible Tokens) are unique digital assets on the blockchain. This guide covers ERC-721, ERC-1155, minting, metadata, and marketplace integration for building NFT-based applications.

## NFT Standards

### ERC-721 (Single NFT)

```solidity
// contracts/MyNFT.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721("MyNFT", "MNFT") {}

    function mintNFT(address recipient, string memory tokenURI)
        public
        onlyOwner
        returns (uint256)
    {
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _safeMint(recipient, newTokenId);
        _setTokenURI(newTokenId, tokenURI);

        return newTokenId;
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}
```

### ERC-1155 (Multi-Token)

```solidity
// contracts/MyMultiToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyMultiToken is ERC1155, Ownable {
    uint256 public constant GOLD = 0;
    uint256 public constant SILVER = 1;
    uint256 public constant BRONZE = 2;

    constructor() ERC1155("https://api.example.com/metadata/{id}.json") {
        _mint(msg.sender, GOLD, 10, "");
        _mint(msg.sender, SILVER, 100, "");
        _mint(msg.sender, BRONZE, 1000, "");
    }

    function mint(
        address account,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) public onlyOwner {
        _mint(account, id, amount, data);
    }

    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) public onlyOwner {
        _mintBatch(to, ids, amounts, data);
    }
}
```

## Minting NFTs

```typescript
// services/nft-minting.service.ts
import { ethers } from 'ethers';
import { NFTStorage, File } from 'nft.storage';

export class NFTMintingService {
  private contract: ethers.Contract;
  private nftStorage: NFTStorage;

  constructor(
    contractAddress: string,
    abi: any[],
    signer: ethers.Signer
  ) {
    this.contract = new ethers.Contract(contractAddress, abi, signer);
    this.nftStorage = new NFTStorage({
      token: process.env.NFT_STORAGE_API_KEY!
    });
  }

  async mintNFT(
    recipient: string,
    metadata: NFTMetadata,
    imageFile: File
  ): Promise<string> {
    // Upload to IPFS
    const metadataURI = await this.uploadMetadata(metadata, imageFile);

    // Mint NFT
    const tx = await this.contract.mintNFT(recipient, metadataURI);
    const receipt = await tx.wait();

    // Get token ID from event
    const event = receipt.events?.find((e: any) => e.event === 'Transfer');
    const tokenId = event?.args?.tokenId.toString();

    return tokenId;
  }

  async uploadMetadata(
    metadata: NFTMetadata,
    imageFile: File
  ): Promise<string> {
    const nft = await this.nftStorage.store({
      name: metadata.name,
      description: metadata.description,
      image: imageFile,
      attributes: metadata.attributes
    });

    return nft.url;
  }

  async batchMint(
    recipients: string[],
    metadataList: NFTMetadata[],
    imageFiles: File[]
  ): Promise<string[]> {
    const tokenIds: string[] = [];

    for (let i = 0; i < recipients.length; i++) {
      const tokenId = await this.mintNFT(
        recipients[i],
        metadataList[i],
        imageFiles[i]
      );
      tokenIds.push(tokenId);
    }

    return tokenIds;
  }
}

interface NFTMetadata {
  name: string;
  description: string;
  attributes: Array<{
    trait_type: string;
    value: string | number;
  }>;
}
```

## NFT Metadata (IPFS)

```typescript
// services/ipfs.service.ts
import { create } from 'ipfs-http-client';
import { NFTStorage } from 'nft.storage';

export class IPFSService {
  private client: any;
  private nftStorage: NFTStorage;

  constructor() {
    // IPFS client
    this.client = create({
      host: 'ipfs.infura.io',
      port: 5001,
      protocol: 'https',
      headers: {
        authorization: `Basic ${Buffer.from(
          `${process.env.INFURA_PROJECT_ID}:${process.env.INFURA_PROJECT_SECRET}`
        ).toString('base64')}`
      }
    });

    // NFT.Storage
    this.nftStorage = new NFTStorage({
      token: process.env.NFT_STORAGE_API_KEY!
    });
  }

  async uploadImage(file: File): Promise<string> {
    const added = await this.client.add(file);
    return `ipfs://${added.path}`;
  }

  async uploadMetadata(metadata: any): Promise<string> {
    const blob = new Blob([JSON.stringify(metadata)], {
      type: 'application/json'
    });
    const added = await this.client.add(blob);
    return `ipfs://${added.path}`;
  }

  async uploadToNFTStorage(
    name: string,
    description: string,
    image: File,
    attributes: any[]
  ): Promise<string> {
    const metadata = await this.nftStorage.store({
      name,
      description,
      image,
      attributes
    });

    return metadata.url;
  }

  getHTTPUrl(ipfsUrl: string): string {
    return ipfsUrl.replace('ipfs://', 'https://ipfs.io/ipfs/');
  }
}
```

## Displaying NFTs

```typescript
// services/nft-display.service.ts
export class NFTDisplayService {
  async getNFTMetadata(tokenURI: string): Promise<NFTMetadata> {
    const httpUrl = tokenURI.replace('ipfs://', 'https://ipfs.io/ipfs/');
    const response = await fetch(httpUrl);
    return response.json();
  }

  async getUserNFTs(
    userAddress: string,
    contractAddress: string,
    provider: ethers.providers.Provider
  ): Promise<NFT[]> {
    const abi = [
      'function balanceOf(address owner) view returns (uint256)',
      'function tokenOfOwnerByIndex(address owner, uint256 index) view returns (uint256)',
      'function tokenURI(uint256 tokenId) view returns (string)'
    ];

    const contract = new ethers.Contract(contractAddress, abi, provider);
    const balance = await contract.balanceOf(userAddress);

    const nfts: NFT[] = [];

    for (let i = 0; i < balance.toNumber(); i++) {
      const tokenId = await contract.tokenOfOwnerByIndex(userAddress, i);
      const tokenURI = await contract.tokenURI(tokenId);
      const metadata = await this.getNFTMetadata(tokenURI);

      nfts.push({
        tokenId: tokenId.toString(),
        tokenURI,
        metadata
      });
    }

    return nfts;
  }
}

interface NFT {
  tokenId: string;
  tokenURI: string;
  metadata: NFTMetadata;
}

// React component
function NFTGallery({ address }: { address: string }) {
  const [nfts, setNfts] = useState<NFT[]>([]);

  useEffect(() => {
    const loadNFTs = async () => {
      const service = new NFTDisplayService();
      const userNFTs = await service.getUserNFTs(
        address,
        CONTRACT_ADDRESS,
        provider
      );
      setNfts(userNFTs);
    };

    loadNFTs();
  }, [address]);

  return (
    <div className="nft-gallery">
      {nfts.map((nft) => (
        <div key={nft.tokenId} className="nft-card">
          <img
            src={nft.metadata.image.replace('ipfs://', 'https://ipfs.io/ipfs/')}
            alt={nft.metadata.name}
          />
          <h3>{nft.metadata.name}</h3>
          <p>{nft.metadata.description}</p>
          <div className="attributes">
            {nft.metadata.attributes.map((attr, i) => (
              <div key={i}>
                <strong>{attr.trait_type}:</strong> {attr.value}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

## NFT Marketplace

```solidity
// contracts/NFTMarketplace.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract NFTMarketplace is ReentrancyGuard {
    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        bool active;
    }

    mapping(bytes32 => Listing) public listings;
    uint256 public listingFee = 0.025 ether;

    event Listed(
        bytes32 indexed listingId,
        address indexed seller,
        address indexed nftContract,
        uint256 tokenId,
        uint256 price
    );

    event Sold(
        bytes32 indexed listingId,
        address indexed buyer,
        uint256 price
    );

    function listNFT(
        address nftContract,
        uint256 tokenId,
        uint256 price
    ) external payable nonReentrant returns (bytes32) {
        require(price > 0, "Price must be greater than 0");
        require(msg.value == listingFee, "Must pay listing fee");

        IERC721 nft = IERC721(nftContract);
        require(nft.ownerOf(tokenId) == msg.sender, "Not the owner");
        require(
            nft.isApprovedForAll(msg.sender, address(this)),
            "Marketplace not approved"
        );

        bytes32 listingId = keccak256(
            abi.encodePacked(nftContract, tokenId, msg.sender, block.timestamp)
        );

        listings[listingId] = Listing({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            price: price,
            active: true
        });

        emit Listed(listingId, msg.sender, nftContract, tokenId, price);

        return listingId;
    }

    function buyNFT(bytes32 listingId) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.active, "Listing not active");
        require(msg.value == listing.price, "Incorrect price");

        listing.active = false;

        // Transfer NFT
        IERC721(listing.nftContract).safeTransferFrom(
            listing.seller,
            msg.sender,
            listing.tokenId
        );

        // Transfer payment
        (bool success, ) = listing.seller.call{value: msg.value}("");
        require(success, "Payment failed");

        emit Sold(listingId, msg.sender, listing.price);
    }

    function cancelListing(bytes32 listingId) external {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not the seller");
        require(listing.active, "Listing not active");

        listing.active = false;
    }
}
```

## Royalties (ERC-2981)

```solidity
// contracts/NFTWithRoyalties.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract NFTWithRoyalties is ERC721, ERC2981 {
    constructor() ERC721("MyNFT", "MNFT") {
        // Set 5% royalty
        _setDefaultRoyalty(msg.sender, 500); // 500 = 5%
    }

    function mint(address to, uint256 tokenId) external {
        _safeMint(to, tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

## OpenSea API

```typescript
// services/opensea.service.ts
export class OpenSeaService {
  private apiKey = process.env.OPENSEA_API_KEY!;
  private baseUrl = 'https://api.opensea.io/api/v1';

  async getAsset(contractAddress: string, tokenId: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/asset/${contractAddress}/${tokenId}`,
      {
        headers: {
          'X-API-KEY': this.apiKey
        }
      }
    );

    return response.json();
  }

  async getAssets(owner: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/assets?owner=${owner}&limit=50`,
      {
        headers: {
          'X-API-KEY': this.apiKey
        }
      }
    );

    return response.json();
  }

  async getCollection(slug: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/collection/${slug}`,
      {
        headers: {
          'X-API-KEY': this.apiKey
        }
      }
    );

    return response.json();
  }

  async getCollectionStats(slug: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/collection/${slug}/stats`,
      {
        headers: {
          'X-API-KEY': this.apiKey
        }
      }
    );

    return response.json();
  }
}
```

## Best Practices

1. **Metadata Standards** - Follow ERC-721/1155 metadata standards
2. **IPFS Storage** - Use IPFS for decentralized storage
3. **Gas Optimization** - Optimize minting costs
4. **Royalties** - Implement ERC-2981 for royalties
5. **Security** - Audit marketplace contracts
6. **Rarity** - Calculate and display rarity
7. **Lazy Minting** - Consider lazy minting for gas savings
8. **Batch Operations** - Support batch minting
9. **Provenance** - Track NFT history
10. **Testing** - Test thoroughly before mainnet

---

## Quick Start

### NFT Minting

```typescript
import { ethers } from 'ethers'

// Mint ERC-721 NFT
async function mintNFT(
  contractAddress: string,
  to: string,
  tokenURI: string
): Promise<string> {
  const contract = new ethers.Contract(
    contractAddress,
    ERC721_ABI,
    signer
  )
  
  const tx = await contract.mint(to, tokenURI)
  await tx.wait()
  
  return tx.hash
}

// Get NFT metadata
async function getNFTMetadata(tokenId: number): Promise<NFTMetadata> {
  const contract = new ethers.Contract(contractAddress, ERC721_ABI, provider)
  const tokenURI = await contract.tokenURI(tokenId)
  
  // Fetch from IPFS
  const metadata = await fetchFromIPFS(tokenURI)
  return metadata
}
```

---

## Production Checklist

- [ ] **NFT Standard**: Choose ERC-721 or ERC-1155
- [ ] **Metadata Standards**: Follow metadata standards
- [ ] **IPFS Storage**: Use IPFS for decentralized storage
- [ ] **Gas Optimization**: Optimize minting costs
- [ ] **Royalties**: Implement ERC-2981 for royalties
- [ ] **Marketplace**: Marketplace integration
- [ ] **Security**: Audit contracts
- [ ] **Testing**: Test on testnets
- [ ] **Documentation**: Document NFT structure
- [ ] **Monitoring**: Monitor minting and transfers
- [ ] **Compliance**: Meet legal requirements
- [ ] **Support**: User support for NFTs

---

## Anti-patterns

### ❌ Don't: Store Metadata On-Chain

```solidity
// ❌ Bad - Store metadata on-chain
struct NFT {
  string name;
  string description;
  string image;
  // Expensive gas costs!
}
```

```solidity
// ✅ Good - Store metadata off-chain (IPFS)
mapping(uint256 => string) public tokenURI;
// Store only URI, metadata on IPFS
```

### ❌ Don't: No Royalties

```solidity
// ❌ Bad - No royalties
function transfer(address to, uint256 tokenId) {
  // Creator gets nothing on resale!
}
```

```solidity
// ✅ Good - ERC-2981 royalties
function royaltyInfo(uint256 tokenId, uint256 salePrice)
  external view returns (address, uint256)
{
  return (creator, salePrice * royaltyPercentage / 10000)
}
```

---

## Integration Points

- **Smart Contracts** (`35-blockchain-web3/smart-contracts/`) - Contract development
- **Wallet Connection** (`35-blockchain-web3/wallet-connection/`) - User wallets
- **Web3 Integration** (`35-blockchain-web3/web3-integration/`) - Web3 patterns

---

## Further Reading

- [ERC-721](https://eips.ethereum.org/EIPS/eip-721)
- [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155)
- [ERC-2981 (Royalties)](https://eips.ethereum.org/EIPS/eip-2981)

---

## Quick Start

### NFT Minting

```typescript
import { ethers } from 'ethers'

// Mint ERC-721 NFT
async function mintNFT(
  contractAddress: string,
  to: string,
  tokenURI: string
): Promise<string> {
  const contract = new ethers.Contract(
    contractAddress,
    ERC721_ABI,
    signer
  )
  
  const tx = await contract.mint(to, tokenURI)
  await tx.wait()
  
  return tx.hash
}

// Get NFT metadata
async function getNFTMetadata(tokenId: number): Promise<NFTMetadata> {
  const contract = new ethers.Contract(contractAddress, ERC721_ABI, provider)
  const tokenURI = await contract.tokenURI(tokenId)
  
  // Fetch from IPFS
  const metadata = await fetchFromIPFS(tokenURI)
  return metadata
}
```

---

## Production Checklist

- [ ] **NFT Standard**: Choose ERC-721 or ERC-1155
- [ ] **Metadata Standards**: Follow metadata standards
- [ ] **IPFS Storage**: Use IPFS for decentralized storage
- [ ] **Gas Optimization**: Optimize minting costs
- [ ] **Royalties**: Implement ERC-2981 for royalties
- [ ] **Marketplace**: Marketplace integration
- [ ] **Security**: Audit contracts
- [ ] **Testing**: Test on testnets
- [ ] **Documentation**: Document NFT structure
- [ ] **Monitoring**: Monitor minting and transfers
- [ ] **Compliance**: Meet legal requirements
- [ ] **Support**: User support for NFTs

---

## Anti-patterns

### ❌ Don't: Store Metadata On-Chain

```solidity
// ❌ Bad - Store metadata on-chain
struct NFT {
  string name;
  string description;
  string image;
  // Expensive gas costs!
}
```

```solidity
// ✅ Good - Store metadata off-chain (IPFS)
mapping(uint256 => string) public tokenURI;
// Store only URI, metadata on IPFS
```

### ❌ Don't: No Royalties

```solidity
// ❌ Bad - No royalties
function transfer(address to, uint256 tokenId) {
  // Creator gets nothing on resale!
}
```

```solidity
// ✅ Good - ERC-2981 royalties
function royaltyInfo(uint256 tokenId, uint256 salePrice)
  external view returns (address, uint256)
{
  return (creator, salePrice * royaltyPercentage / 10000)
}
```

---

## Integration Points

- **Smart Contracts** (`35-blockchain-web3/smart-contracts/`) - Contract development
- **Wallet Connection** (`35-blockchain-web3/wallet-connection/`) - User wallets
- **Web3 Integration** (`35-blockchain-web3/web3-integration/`) - Web3 patterns

---

## Further Reading

- [ERC-721](https://eips.ethereum.org/EIPS/eip-721)
- [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155)
- [ERC-2981 (Royalties)](https://eips.ethereum.org/EIPS/eip-2981)

## Resources
- [NFT.Storage](https://nft.storage/)
- [OpenSea API](https://docs.opensea.io/)
- [ERC-2981 Royalties](https://eips.ethereum.org/EIPS/eip-2981)
