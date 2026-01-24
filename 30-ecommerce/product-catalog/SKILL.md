---
name: Product Catalog Management
description: Managing product data, variants, categories, pricing rules, and search functionality for e-commerce platforms with proper data modeling, search optimization, and SEO.
---

# Product Catalog Management

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Backend

---

## Overview

Product catalog management handles product data, variants, categories, pricing rules, and search functionality for e-commerce platforms. Effective catalog systems provide fast search, flexible product variants, proper categorization, and SEO optimization.

---

## Core Concepts

### Table of Contents

1. [Product Data Model](#product-data-model)
2. [Product Attributes](#product-attributes)
3. [Variants and Options](#variants-and-options)
4. [Categories and Tags](#categories-and-tags)
5. [Product Search](#product-search)
6. [Filters and Facets](#filters-and-facets)
7. [Product Recommendations](#product-recommendations)
8. [Image Management](#image-management)
9. [SEO Optimization](#seo-optimization)
10. [Pricing Rules](#pricing-rules)
11. [Bulk Operations](#bulk-operations)
12. [Import/Export](#importexport)
13. [Database Schema](#database-schema)
14. [Best Practices](#best-practices)

---

## Product Data Model

### Product Types

```typescript
enum ProductType {
  SIMPLE = 'simple',        // Single product with no variants
  VARIABLE = 'variable',    // Product with variants
  BUNDLE = 'bundle',        // Bundle of multiple products
  DIGITAL = 'digital',      // Digital download
  GIFT_CARD = 'gift_card',  // Gift card
  SUBSCRIPTION = 'subscription', // Subscription product
}

enum ProductStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  ARCHIVED = 'archived',
  OUT_OF_STOCK = 'out_of_stock',
}
```

### Product Manager

```typescript
class ProductManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create product
   */
  async createProduct(params: {
    name: string;
    description?: string;
    shortDescription?: string;
    type: ProductType;
    sku: string;
    price: number;
    salePrice?: number;
    cost?: number;
    taxClass?: string;
    stockQuantity?: number;
    lowStockThreshold?: number;
    allowBackorders?: boolean;
    requiresShipping?: boolean;
    weight?: number;
    length?: number;
    width?: number;
    height?: number;
    categoryIds?: string[];
    tagIds?: string[];
    attributeValues?: Record<string, string>;
    images?: Array<{
      url: string;
      alt?: string;
      position?: number;
    }>;
    seoTitle?: string;
    seoDescription?: string;
    seoKeywords?: string[];
    status?: ProductStatus;
  }): Promise<Product> {
    return await this.prisma.$transaction(async (tx) => {
      // Create product
      const product = await tx.product.create({
        data: {
          name: params.name,
          description: params.description,
          shortDescription: params.shortDescription,
          type: params.type,
          sku: params.sku,
          price: params.price,
          salePrice: params.salePrice,
          cost: params.cost,
          taxClass: params.taxClass,
          stockQuantity: params.stockQuantity || 0,
          lowStockThreshold: params.lowStockThreshold || 10,
          allowBackorders: params.allowBackorders || false,
          requiresShipping: params.requiresShipping !== false,
          weight: params.weight,
          length: params.length,
          width: params.width,
          height: params.height,
          seoTitle: params.seoTitle,
          seoDescription: params.seoDescription,
          seoKeywords: params.seoKeywords,
          status: params.status || ProductStatus.DRAFT,
        },
      });

      // Add categories
      if (params.categoryIds && params.categoryIds.length > 0) {
        await tx.productCategory.createMany({
          data: params.categoryIds.map(categoryId => ({
            productId: product.id,
            categoryId,
          })),
        });
      }

      // Add tags
      if (params.tagIds && params.tagIds.length > 0) {
        await tx.productTag.createMany({
          data: params.tagIds.map(tagId => ({
            productId: product.id,
            tagId,
          })),
        });
      }

      // Add attribute values
      if (params.attributeValues) {
        for (const [key, value] of Object.entries(params.attributeValues)) {
          await tx.productAttributeValue.create({
            data: {
              productId: product.id,
              attributeKey: key,
              value,
            },
          });
        }
      }

      // Add images
      if (params.images && params.images.length > 0) {
        await tx.productImage.createMany({
          data: params.images.map((image, index) => ({
            productId: product.id,
            url: image.url,
            alt: image.alt,
            position: image.position || index,
          })),
        });
      }

      return product;
    });
  }

  /**
   * Update product
   */
  async updateProduct(
    productId: string,
    params: Partial<ReturnType<typeof ProductManager.prototype.createProduct>>
  ): Promise<Product> {
    return await this.prisma.$transaction(async (tx) => {
      // Update product
      const product = await tx.product.update({
        where: { id: productId },
        data: {
          name: params.name,
          description: params.description,
          shortDescription: params.shortDescription,
          sku: params.sku,
          price: params.price,
          salePrice: params.salePrice,
          cost: params.cost,
          taxClass: params.taxClass,
          stockQuantity: params.stockQuantity,
          lowStockThreshold: params.lowStockThreshold,
          allowBackorders: params.allowBackorders,
          requiresShipping: params.requiresShipping,
          weight: params.weight,
          length: params.length,
          width: params.width,
          height: params.height,
          seoTitle: params.seoTitle,
          seoDescription: params.seoDescription,
          seoKeywords: params.seoKeywords,
          status: params.status,
        },
      });

      // Update categories
      if (params.categoryIds !== undefined) {
        await tx.productCategory.deleteMany({ productId });
        await tx.productCategory.createMany({
          data: params.categoryIds.map(categoryId => ({
            productId,
            categoryId,
          })),
        });
      }

      // Update tags
      if (params.tagIds !== undefined) {
        await tx.productTag.deleteMany({ productId });
        await tx.productTag.createMany({
          data: params.tagIds.map(tagId => ({
            productId,
            tagId,
          })),
        });
      }

      return product;
    });
  }

  /**
   * Delete product
   */
  async deleteProduct(productId: string): Promise<void> {
    await this.prisma.product.delete({
      where: { id: productId },
    });
  }

  /**
   * Get product
   */
  async getProduct(productId: string): Promise<Product | null> {
    return await this.prisma.product.findUnique({
      where: { id: productId },
      include: {
        categories: {
          include: { category: true },
        },
        tags: {
          include: { tag: true },
        },
        variants: {
          include: {
            attributeValues: true,
          },
        },
        images: {
          orderBy: { position: 'asc' },
        },
        attributeValues: true,
      },
    });
  }

  /**
   * List products
   */
  async listProducts(params: {
    page?: number;
    limit?: number;
    categoryIds?: string[];
    tagIds?: string[];
    status?: ProductStatus;
    type?: ProductType;
    search?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }): Promise<{
    products: Product[];
    total: number;
    page: number;
    totalPages: number;
  }> {
    const where: any = {};

    if (params.categoryIds && params.categoryIds.length > 0) {
      where.categories = {
        some: {
          categoryId: { in: params.categoryIds },
        },
      };
    }

    if (params.tagIds && params.tagIds.length > 0) {
      where.tags = {
        some: {
          tagId: { in: params.tagIds },
        },
      };
    }

    if (params.status) {
      where.status = params.status;
    }

    if (params.type) {
      where.type = params.type;
    }

    if (params.search) {
      where.OR = [
        { name: { contains: params.search, mode: 'insensitive' } },
        { description: { contains: params.search, mode: 'insensitive' } },
        { sku: { contains: params.search, mode: 'insensitive' } },
      ];
    }

    const page = params.page || 1;
    const limit = params.limit || 20;
    const skip = (page - 1) * limit;

    const [products, total] = await Promise.all([
      this.prisma.product.findMany({
        where,
        include: {
          categories: {
            include: { category: true },
          },
          tags: {
            include: { tag: true },
          },
          images: {
            orderBy: { position: 'asc' },
            take: 1,
          },
        },
        orderBy: {
          [params.sortBy || 'createdAt']: params.sortOrder || 'desc',
        },
        skip,
        take: limit,
      }),
      this.prisma.product.count({ where }),
    ]);

    return {
      products,
      total,
      page,
      totalPages: Math.ceil(total / limit),
    };
  }
}
```

---

## Product Attributes

### Attribute Manager

```typescript
class AttributeManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create attribute
   */
  async createAttribute(params: {
    name: string;
    code: string;
    type: 'text' | 'number' | 'select' | 'multiselect' | 'boolean' | 'date';
    options?: string[];
    required?: boolean;
    searchable?: boolean;
    filterable?: boolean;
  }): Promise<Attribute> {
    return await this.prisma.attribute.create({
      data: {
        name: params.name,
        code: params.code,
        type: params.type,
        options: params.options,
        required: params.required || false,
        searchable: params.searchable || false,
        filterable: params.filterable || false,
      },
    });
  }

  /**
   * Get attributes
   */
  async getAttributes(): Promise<Attribute[]> {
    return await this.prisma.attribute.findMany({
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Get attribute values for product
   */
  async getProductAttributeValues(productId: string): Promise<Record<string, string>> {
    const values = await this.prisma.productAttributeValue.findMany({
      where: { productId },
    });

    return values.reduce((acc, v) => {
      acc[v.attributeKey] = v.value;
      return acc;
    }, {} as Record<string, string>);
  }

  /**
   * Set attribute values for product
   */
  async setAttributeValues(
    productId: string,
    values: Record<string, string>
  ): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      // Delete existing values
      await tx.productAttributeValue.deleteMany({ productId });

      // Create new values
      await tx.productAttributeValue.createMany({
        data: Object.entries(values).map(([key, value]) => ({
          productId,
          attributeKey: key,
          value,
        })),
      });
    });
  }
}
```

---

## Variants and Options

### Variant Manager

```typescript
class VariantManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create variant
   */
  async createVariant(params: {
    productId: string;
    sku: string;
    price?: number;
    salePrice?: number;
    cost?: number;
    stockQuantity?: number;
    weight?: number;
    length?: number;
    width?: number;
    height?: number;
    attributeValues: Record<string, string>;
    images?: Array<{
      url: string;
      alt?: string;
      position?: number;
    }>;
  }): Promise<Variant> {
    return await this.prisma.$transaction(async (tx) => {
      // Create variant
      const variant = await tx.variant.create({
        data: {
          productId: params.productId,
          sku: params.sku,
          price: params.price,
          salePrice: params.salePrice,
          cost: params.cost,
          stockQuantity: params.stockQuantity || 0,
          weight: params.weight,
          length: params.length,
          width: params.width,
          height: params.height,
        },
      });

      // Add attribute values
      for (const [key, value] of Object.entries(params.attributeValues)) {
        await tx.variantAttributeValue.create({
          data: {
            variantId: variant.id,
            attributeKey: key,
            value,
          },
        });
      }

      // Add images
      if (params.images && params.images.length > 0) {
        await tx.variantImage.createMany({
          data: params.images.map((image, index) => ({
            variantId: variant.id,
            url: image.url,
            alt: image.alt,
            position: image.position || index,
          })),
        });
      }

      return variant;
    });
  }

  /**
   * Generate variants from options
   */
  async generateVariants(productId: string, options: Record<string, string[]>): Promise<Variant[]> {
    const product = await this.prisma.product.findUnique({
      where: { id: productId },
    });

    if (!product) {
      throw new Error('Product not found');
    }

    // Generate all combinations
    const combinations = this.generateCombinations(options);
    const variants: Variant[] = [];

    for (const combination of combinations) {
      const sku = `${product.sku}-${Object.values(combination).join('-')}`;

      const variant = await this.createVariant({
        productId,
        sku,
        attributeValues: combination,
      });

      variants.push(variant);
    }

    return variants;
  }

  /**
   * Generate combinations
   */
  private generateCombinations(options: Record<string, string[]>): Array<Record<string, string>> {
    const keys = Object.keys(options);
    const values = Object.values(options);

    const combinations: Array<Record<string, string>> = [];

    const generate = (index: number, current: Record<string, string>) => {
      if (index === keys.length) {
        combinations.push({ ...current });
        return;
      }

      for (const value of values[index]) {
        current[keys[index]] = value;
        generate(index + 1, current);
      }
    };

    generate(0, {});
    return combinations;
  }

  /**
   * Get variant
   */
  async getVariant(variantId: string): Promise<Variant | null> {
    return await this.prisma.variant.findUnique({
      where: { id: variantId },
      include: {
        attributeValues: true,
        images: {
          orderBy: { position: 'asc' },
        },
      },
    });
  }
}
```

---

## Categories and Tags

### Category Manager

```typescript
class CategoryManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create category
   */
  async createCategory(params: {
    name: string;
    slug: string;
    description?: string;
    parentId?: string;
    image?: string;
    seoTitle?: string;
    seoDescription?: string;
  }): Promise<Category> {
    return await this.prisma.category.create({
      data: {
        name: params.name,
        slug: params.slug,
        description: params.description,
        parentId: params.parentId,
        image: params.image,
        seoTitle: params.seoTitle,
        seoDescription: params.seoDescription,
      },
    });
  }

  /**
   * Get category tree
   */
  async getCategoryTree(): Promise<CategoryNode[]> {
    const categories = await this.prisma.category.findMany({
      where: { parentId: null },
      include: {
        children: {
          include: {
            children: true,
          },
        },
      },
      orderBy: { name: 'asc' },
    });

    return categories.map(this.buildCategoryNode);
  }

  /**
   * Build category node
   */
  private buildCategoryNode(category: any): CategoryNode {
    return {
      id: category.id,
      name: category.name,
      slug: category.slug,
      image: category.image,
      children: category.children?.map((c: any) => this.buildCategoryNode(c)) || [],
    };
  }

  /**
   * Update category
   */
  async updateCategory(
    categoryId: string,
    params: Partial<ReturnType<typeof CategoryManager.prototype.createCategory>>
  ): Promise<Category> {
    return await this.prisma.category.update({
      where: { id: categoryId },
      data: params,
    });
  }

  /**
   * Delete category
   */
  async deleteCategory(categoryId: string): Promise<void> {
    await this.prisma.category.delete({
      where: { id: categoryId },
    });
  }
}

interface CategoryNode {
  id: string;
  name: string;
  slug: string;
  image?: string;
  children: CategoryNode[];
}
```

### Tag Manager

```typescript
class TagManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create tag
   */
  async createTag(params: {
    name: string;
    slug: string;
  }): Promise<Tag> {
    return await this.prisma.tag.create({
      data: {
        name: params.name,
        slug: params.slug,
      },
    });
  }

  /**
   * Get tags
   */
  async getTags(): Promise<Tag[]> {
    return await this.prisma.tag.findMany({
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Update tag
   */
  async updateTag(tagId: string, params: Partial<{ name: string; slug: string }>): Promise<Tag> {
    return await this.prisma.tag.update({
      where: { id: tagId },
      data: params,
    });
  }

  /**
   * Delete tag
   */
  async deleteTag(tagId: string): Promise<void> {
    await this.prisma.tag.delete({
      where: { id: tagId },
    });
  }
}
```

---

## Product Search

### Search Manager

```typescript
class SearchManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Search products
   */
  async searchProducts(params: {
    query: string;
    categoryIds?: string[];
    tagIds?: string[];
    minPrice?: number;
    maxPrice?: number;
    inStock?: boolean;
    page?: number;
    limit?: number;
  }): Promise<{
    products: Product[];
    total: number;
    facets: Facet[];
  }> {
    const where: any = {
      status: ProductStatus.ACTIVE,
    };

    // Search query
    if (params.query) {
      where.OR = [
        { name: { contains: params.query, mode: 'insensitive' } },
        { description: { contains: params.query, mode: 'insensitive' } },
        { sku: { contains: params.query, mode: 'insensitive' } },
      ];
    }

    // Category filter
    if (params.categoryIds && params.categoryIds.length > 0) {
      where.categories = {
        some: {
          categoryId: { in: params.categoryIds },
        },
      };
    }

    // Tag filter
    if (params.tagIds && params.tagIds.length > 0) {
      where.tags = {
        some: {
          tagId: { in: params.tagIds },
        },
      };
    }

    // Price filter
    if (params.minPrice !== undefined || params.maxPrice !== undefined) {
      where.price = {};
      if (params.minPrice !== undefined) {
        where.price.gte = params.minPrice;
      }
      if (params.maxPrice !== undefined) {
        where.price.lte = params.maxPrice;
      }
    }

    // Stock filter
    if (params.inStock) {
      where.stockQuantity = { gt: 0 };
    }

    const page = params.page || 1;
    const limit = params.limit || 20;
    const skip = (page - 1) * limit;

    const [products, total] = await Promise.all([
      this.prisma.product.findMany({
        where,
        include: {
          categories: {
            include: { category: true },
          },
          tags: {
            include: { tag: true },
          },
          images: {
            orderBy: { position: 'asc' },
            take: 1,
          },
        },
        orderBy: { name: 'asc' },
        skip,
        take: limit,
      }),
      this.prisma.product.count({ where }),
    ]);

    // Generate facets
    const facets = await this.generateFacets(where);

    return {
      products,
      total,
      facets,
    };
  }

  /**
   * Generate facets
   */
  private async generateFacets(where: any): Promise<Facet[]> {
    const facets: Facet[] = [];

    // Category facet
    const categories = await this.prisma.category.findMany({
      where: {
        products: { some: where },
      },
      include: {
        _count: {
          select: { products: { where } },
        },
      },
      orderBy: { name: 'asc' },
    });

    facets.push({
      name: 'Category',
      type: 'category',
      options: categories.map(c => ({
        id: c.id,
        name: c.name,
        count: c._count.products,
      })),
    });

    // Tag facet
    const tags = await this.prisma.tag.findMany({
      where: {
        products: { some: where },
      },
      include: {
        _count: {
          select: { products: { where } },
        },
      },
      orderBy: { name: 'asc' },
    });

    facets.push({
      name: 'Tags',
      type: 'tag',
      options: tags.map(t => ({
        id: t.id,
        name: t.name,
        count: t._count.products,
      })),
    });

    return facets;
  }
}

interface Facet {
  name: string;
  type: string;
  options: Array<{
    id: string;
    name: string;
    count: number;
  }>;
}
```

---

## Filters and Facets

### Filter Manager

```typescript
class FilterManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get available filters
   */
  async getFilters(): Promise<Filter[]> {
    const attributes = await this.prisma.attribute.findMany({
      where: { filterable: true },
      include: {
        _count: {
          select: { productValues: true },
        },
      },
    });

    return attributes.map(attr => ({
      id: attr.id,
      name: attr.name,
      code: attr.code,
      type: attr.type,
      options: attr.options,
      count: attr._count.productValues,
    }));
  }

  /**
   * Get filter values
   */
  async getFilterValues(params: {
    attributeCode: string;
    categoryIds?: string[];
  }): Promise<Array<{ value: string; count: number }>> {
    const where: any = {
      attributeKey: params.attributeCode,
    };

    if (params.categoryIds && params.categoryIds.length > 0) {
      where.product = {
        categories: {
          some: {
            categoryId: { in: params.categoryIds },
          },
        },
      };
    }

    const values = await this.prisma.productAttributeValue.groupBy({
      by: ['value'],
      where,
      _count: true,
      orderBy: { _count: { value: 'desc' } },
    });

    return values.map(v => ({
      value: v.value,
      count: v._count,
    }));
  }
}

interface Filter {
  id: string;
  name: string;
  code: string;
  type: string;
  options?: string[];
  count: number;
}
```

---

## Product Recommendations

### Recommendation Engine

```typescript
class RecommendationEngine {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get related products
   */
  async getRelatedProducts(
    productId: string,
    limit: number = 4
  ): Promise<Product[]> {
    const product = await this.prisma.product.findUnique({
      where: { id: productId },
      include: {
        categories: true,
        tags: true,
      },
    });

    if (!product) {
      return [];
    }

    // Get products in same categories
    const categoryIds = product.categories.map(c => c.categoryId);
    const tagIds = product.tags.map(t => t.tagId);

    const related = await this.prisma.product.findMany({
      where: {
        id: { not: productId },
        status: ProductStatus.ACTIVE,
        OR: [
          {
            categories: {
              some: {
                categoryId: { in: categoryIds },
              },
            },
          },
          {
            tags: {
              some: {
                tagId: { in: tagIds },
              },
            },
          },
        ],
      },
      include: {
        images: {
          orderBy: { position: 'asc' },
          take: 1,
        },
      },
      take: limit,
    });

    return related;
  }

  /**
   * Get frequently bought together
   */
  async getFrequentlyBoughtTogether(
    productId: string,
    limit: number = 4
  ): Promise<Product[]> {
    // Get orders containing this product
    const orders = await this.prisma.orderItem.findMany({
      where: { productId },
      select: { orderId: true },
      distinct: ['orderId'],
    });

    const orderIds = orders.map(o => o.orderId);

    // Get other products in those orders
    const otherProducts = await this.prisma.orderItem.groupBy({
      by: ['productId'],
      where: {
        orderId: { in: orderIds },
        productId: { not: productId },
      },
      _count: true,
      orderBy: { _count: { productId: 'desc' } },
      take: limit,
    });

    const productIds = otherProducts.map(p => p.productId);

    const products = await this.prisma.product.findMany({
      where: {
        id: { in: productIds },
        status: ProductStatus.ACTIVE,
      },
      include: {
        images: {
          orderBy: { position: 'asc' },
          take: 1,
        },
      },
    });

    // Sort by frequency
    const productMap = new Map(products.map(p => [p.id, p]));
    const sorted = otherProducts
      .sort((a, b) => b._count - a._count)
      .map(p => productMap.get(p.productId))
      .filter(Boolean);

    return sorted as Product[];
  }

  /**
   * Get personalized recommendations
   */
  async getPersonalizedRecommendations(
    userId: string,
    limit: number = 10
  ): Promise<Product[]> {
    // Get user's purchase history
    const purchases = await this.prisma.orderItem.findMany({
      where: {
        order: {
          userId,
          status: OrderStatus.DELIVERED,
        },
      },
      select: { productId: true },
      distinct: ['productId'],
    });

    const purchasedIds = purchases.map(p => p.productId);

    // Get related products
    const recommendations: Product[] = [];

    for (const productId of purchasedIds) {
      const related = await this.getRelatedProducts(productId, 2);
      recommendations.push(...related);
    }

    // Remove duplicates and already purchased
    const unique = new Map<string, Product>();

    for (const product of recommendations) {
      if (!unique.has(product.id) && !purchasedIds.includes(product.id)) {
        unique.set(product.id, product);
      }
    }

    return Array.from(unique.values()).slice(0, limit);
  }
}
```

---

## Image Management

### Image Manager

```typescript
class ImageManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Upload product image
   */
  async uploadProductImage(params: {
    productId: string;
    file: Buffer;
    filename: string;
    alt?: string;
    position?: number;
  }): Promise<ProductImage> {
    // Upload to storage
    const url = await this.uploadToStorage(params.file, params.filename);

    // Create image record
    const image = await this.prisma.productImage.create({
      data: {
        productId: params.productId,
        url,
        alt: params.alt,
        position: params.position || 0,
      },
    });

    return image;
  }

  /**
   * Upload variant image
   */
  async uploadVariantImage(params: {
    variantId: string;
    file: Buffer;
    filename: string;
    alt?: string;
    position?: number;
  }): Promise<VariantImage> {
    const url = await this.uploadToStorage(params.file, params.filename);

    const image = await this.prisma.variantImage.create({
      data: {
        variantId: params.variantId,
        url,
        alt: params.alt,
        position: params.position || 0,
      },
    });

    return image;
  }

  /**
   * Upload to storage
   */
  private async uploadToStorage(file: Buffer, filename: string): Promise<string> {
    // Implement storage upload (S3, Cloudinary, etc.)
    return `https://cdn.example.com/${filename}`;
  }

  /**
   * Delete image
   */
  async deleteImage(imageId: string): Promise<void> {
    await this.prisma.productImage.delete({
      where: { id: imageId },
    });
  }

  /**
   * Reorder images
   */
  async reorderImages(params: Array<{
    imageId: string;
    position: number;
  }>): Promise<void> {
    for (const { imageId, position } of params) {
      await this.prisma.productImage.update({
        where: { id: imageId },
        data: { position },
      });
    }
  }
}
```

---

## SEO Optimization

### SEO Manager

```typescript
class SEOManager {
  /**
   * Generate SEO meta tags
   */
  generateMetaTags(product: Product): {
    title: string;
    description: string;
    keywords: string[];
    ogTags: Record<string, string>;
  } {
    const title = product.seoTitle || product.name;
    const description = product.seoDescription || product.shortDescription || product.description?.substring(0, 160);
    const keywords = product.seoKeywords || this.extractKeywords(product);

    const ogTags = {
      'og:title': title,
      'og:description': description.substring(0, 160),
      'og:type': 'product',
      'og:image': product.images[0]?.url || '',
      'product:price:amount': product.salePrice || product.price,
      'product:price:currency': 'USD',
    };

    return {
      title,
      description,
      keywords,
      ogTags,
    };
  }

  /**
   * Extract keywords
   */
  private extractKeywords(product: Product): string[] {
    const text = `${product.name} ${product.description || ''}`;
    const words = text.toLowerCase().split(/\s+/);
    const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']);

    return [...new Set(words.filter(w => w.length > 3 && !stopWords.has(w)))];
  }

  /**
   * Generate sitemap
   */
  async generateSitemap(): Promise<string> {
    const products = await this.prisma.product.findMany({
      where: { status: ProductStatus.ACTIVE },
      select: {
        id: true,
        updatedAt: true,
      },
    });

    const urls = products.map(p => `
      <url>
        <loc>${process.env.APP_URL}/products/${p.id}</loc>
        <lastmod>${p.updatedAt.toISOString()}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
      </url>
    `).join('');

    return `<?xml version="1.0" encoding="UTF-8"?>
      <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        ${urls}
      </urlset>
    `;
  }
}
```

---

## Pricing Rules

### Pricing Manager

```typescript
class PricingManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get product price
   */
  async getProductPrice(
    productId: string,
    variantId?: string,
    userId?: string
  ): Promise<{
    price: number;
    salePrice?: number;
    discount?: number;
  }> {
    const product = await this.prisma.product.findUnique({
      where: { id: productId },
    });

    if (!product) {
      throw new Error('Product not found');
    }

    let price = product.price;
    let salePrice = product.salePrice;

    // Check variant price
    if (variantId) {
      const variant = await this.prisma.variant.findUnique({
        where: { id: variantId },
      });

      if (variant) {
        price = variant.price || price;
        salePrice = variant.salePrice || salePrice;
      }
    }

    // Apply pricing rules
    const discount = await this.applyPricingRules(productId, userId);

    return {
      price,
      salePrice: salePrice || undefined,
      discount,
    };
  }

  /**
   * Apply pricing rules
   */
  private async applyPricingRules(
    productId: string,
    userId?: string
  ): Promise<number | undefined> {
    // Get active pricing rules
    const rules = await this.prisma.pricingRule.findMany({
      where: {
        active: true,
        OR: [
          { productIds: { has: productId } },
          { categoryIds: { isEmpty: true } }, // Global rules
        ],
      },
      include: {
        conditions: true,
      },
    });

    let maxDiscount = 0;

    for (const rule of rules) {
      if (this.matchesConditions(rule, userId)) {
        maxDiscount = Math.max(maxDiscount, rule.discount);
      }
    }

    return maxDiscount > 0 ? maxDiscount : undefined;
  }

  /**
   * Check if rule conditions match
   */
  private matchesConditions(rule: any, userId?: string): boolean {
    // Implement condition matching
    return true;
  }
}
```

---

## Bulk Operations

### Bulk Operations Manager

```typescript
class BulkOperationsManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Bulk update products
   */
  async bulkUpdateProducts(params: {
    productIds: string[];
    updates: Partial<{
      price: number;
      salePrice: number;
      stockQuantity: number;
      status: ProductStatus;
    }>;
  }): Promise<{ success: string[]; failed: Array<{ productId: string; error: string }> }> {
    const success: string[] = [];
    const failed: Array<{ productId: string; error: string }> = [];

    for (const productId of params.productIds) {
      try {
        await this.prisma.product.update({
          where: { id: productId },
          data: params.updates,
        });
        success.push(productId);
      } catch (error) {
        failed.push({
          productId,
          error: error.message,
        });
      }
    }

    return { success, failed };
  }

  /**
   * Bulk delete products
   */
  async bulkDeleteProducts(productIds: string[]): Promise<{
    success: string[];
    failed: Array<{ productId: string; error: string }>;
  }> {
    const success: string[] = [];
    const failed: Array<{ productId: string; error: string }> = [];

    for (const productId of productIds) {
      try {
        await this.prisma.product.delete({
          where: { id: productId },
        });
        success.push(productId);
      } catch (error) {
        failed.push({
          productId,
          error: error.message,
        });
      }
    }

    return { success, failed };
  }
}
```

---

## Import/Export

### Import Export Manager

```typescript
class ImportExportManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Export products
   */
  async exportProducts(params?: {
    categoryIds?: string[];
    status?: ProductStatus;
  }): Promise<Buffer> {
    const where: any = {};

    if (params?.categoryIds && params.categoryIds.length > 0) {
      where.categories = {
        some: {
          categoryId: { in: params.categoryIds },
        },
      };
    }

    if (params?.status) {
      where.status = params.status;
    }

    const products = await this.prisma.product.findMany({
      where,
      include: {
        variants: true,
        categories: {
          include: { category: true },
        },
        tags: {
          include: { tag: true },
        },
        images: {
          orderBy: { position: 'asc' },
        },
      },
    });

    const csv = this.convertToCSV(products);
    return Buffer.from(csv);
  }

  /**
   * Import products
   */
  async importProducts(file: Buffer): Promise<{
    imported: number;
    failed: number;
    errors: Array<{ row: number; error: string }>;
  }> {
    const data = this.parseCSV(file.toString());

    let imported = 0;
    let failed = 0;
    const errors: Array<{ row: number; error: string }> = [];

    for (let i = 0; i < data.length; i++) {
      try {
        await this.importProduct(data[i]);
        imported++;
      } catch (error) {
        failed++;
        errors.push({
          row: i + 1,
          error: error.message,
        });
      }
    }

    return { imported, failed, errors };
  }

  /**
   * Convert to CSV
   */
  private convertToCSV(products: any[]): string {
    const headers = [
      'ID',
      'Name',
      'SKU',
      'Price',
      'Sale Price',
      'Stock Quantity',
      'Status',
      'Categories',
      'Tags',
      'Description',
    ];

    const rows = products.map(p => [
      p.id,
      p.name,
      p.sku,
      p.price,
      p.salePrice || '',
      p.stockQuantity,
      p.status,
      p.categories.map((c: any) => c.category.name).join(', '),
      p.tags.map((t: any) => t.tag.name).join(', '),
      p.description?.replace(/"/g, '""') || '',
    ]);

    return [
      headers.join(','),
      ...rows.map(r => r.map(v => `"${v}"`).join(',')),
    ].join('\n');
  }

  /**
   * Parse CSV
   */
  private parseCSV(csv: string): any[] {
    const lines = csv.split('\n');
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));

    return lines.slice(1).map(line => {
      const values = line.split(',').map(v => v.trim().replace(/"/g, ''));
      const obj: any = {};

      headers.forEach((h, i) => {
        obj[h] = values[i];
      });

      return obj;
    });
  }

  /**
   * Import product
   */
  private async importProduct(data: any): Promise<void> {
    const productManager = new ProductManager(this.prisma);

    await productManager.createProduct({
      name: data.Name,
      sku: data.SKU,
      price: parseFloat(data.Price),
      salePrice: data['Sale Price'] ? parseFloat(data['Sale Price']) : undefined,
      stockQuantity: parseInt(data['Stock Quantity']) || 0,
      status: data.Status as ProductStatus,
    });
  }
}
```

---

## Database Schema

### Prisma Schema

```prisma
model Product {
  id                String                @id @default(uuid())
  name              String
  description        String?
  shortDescription   String?
  type              ProductType           @default(SIMPLE)
  sku               String                @unique
  price             Decimal
  salePrice         Decimal?
  cost              Decimal?
  taxClass          String?
  stockQuantity     Int                   @default(0)
  lowStockThreshold Int                   @default(10)
  allowBackorders   Boolean               @default(false)
  requiresShipping  Boolean               @default(true)
  weight            Decimal?
  length            Decimal?
  width             Decimal?
  height            Decimal?
  seoTitle          String?
  seoDescription    String?
  seoKeywords       String[]
  status            ProductStatus         @default(DRAFT)
  createdAt         DateTime              @default(now())
  updatedAt         DateTime              @updatedAt
  categories        ProductCategory[]
  tags              ProductTag[]
  variants          Variant[]
  images            ProductImage[]
  attributeValues   ProductAttributeValue[]
  orderItems        OrderItem[]
  inventory         Inventory[]
  pricingRules      PricingRule[]

  @@index([sku])
  @@index([status])
  @@index([type])
}

model Variant {
  id              String                @id @default(uuid())
  productId       String
  product         Product               @relation(fields: [productId], references: [id], onDelete: Cascade)
  sku             String                @unique
  price           Decimal?
  salePrice       Decimal?
  cost            Decimal?
  stockQuantity   Int                   @default(0)
  weight          Decimal?
  length          Decimal?
  width           Decimal?
  height          Decimal?
  createdAt       DateTime              @default(now())
  updatedAt       DateTime              @updatedAt
  attributeValues VariantAttributeValue[]
  images          VariantImage[]
  orderItems      OrderItem[]
  inventory       Inventory[]

  @@index([sku])
  @@index([productId])
}

model Category {
  id               String         @id @default(uuid())
  name             String
  slug             String        @unique
  description      String?
  parentId         String?
  parent           Category?      @relation("CategoryToCategory", fields: [parentId], references: [id])
  children         Category[]     @relation("CategoryToCategory")
  image            String?
  seoTitle         String?
  seoDescription   String?
  products         ProductCategory[]
  createdAt        DateTime       @default(now())
  updatedAt        DateTime       @updatedAt

  @@index([slug])
  @@index([parentId])
}

model Tag {
  id        String       @id @default(uuid())
  name      String
  slug      String      @unique
  products  ProductTag[]
  createdAt DateTime    @default(now())
  updatedAt DateTime    @updatedAt

  @@index([slug])
}

model Attribute {
  id          String   @id @default(uuid())
  name        String
  code        String   @unique
  type        String   // text, number, select, multiselect, boolean, date
  options     String[]
  required    Boolean  @default(false)
  searchable  Boolean  @default(false)
  filterable  Boolean  @default(false)
  productValues ProductAttributeValue[]
  variantValues VariantAttributeValue[]

  @@index([code])
}

model ProductImage {
  id        String   @id @default(uuid())
  productId String
  product   Product  @relation(fields: [productId], references: [id], onDelete: Cascade)
  url       String
  alt       String?
  position  Int      @default(0)
  createdAt DateTime @default(now())

  @@index([productId])
}

model VariantImage {
  id        String   @id @default(uuid())
  variantId String
  variant   Variant  @relation(fields: [variantId], references: [id], onDelete: Cascade)
  url       String
  alt       String?
  position  Int      @default(0)
  createdAt DateTime @default(now())

  @@index([variantId])
}

model ProductCategory {
  id         String   @id @default(uuid())
  productId  String
  product    Product  @relation(fields: [productId], references: [id], onDelete: Cascade)
  categoryId String
  category   Category @relation(fields: [categoryId], references: [id], onDelete: Cascade)

  @@unique([productId, categoryId])
  @@index([productId])
  @@index([categoryId])
}

model ProductTag {
  id        String   @id @default(uuid())
  productId String
  product   Product  @relation(fields: [productId], references: [id], onDelete: Cascade)
  tagId     String
  tag       Tag      @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@unique([productId, tagId])
  @@index([productId])
  @@index([tagId])
}

model ProductAttributeValue {
  id           String   @id @default(uuid())
  productId    String
  product      Product  @relation(fields: [productId], references: [id], onDelete: Cascade)
  attributeKey String
  value        String

  @@unique([productId, attributeKey])
  @@index([productId])
}

model VariantAttributeValue {
  id           String   @id @default(uuid())
  variantId    String
  variant      Variant  @relation(fields: [variantId], references: [id], onDelete: Cascade)
  attributeKey String
  value        String

  @@unique([variantId, attributeKey])
  @@index([variantId])
}
```

---

## Best Practices

### Product Catalog Best Practices

```typescript
// 1. Use unique SKUs
async function validateSKU(sku: string): Promise<boolean> {
  const existing = await prisma.product.findFirst({
    where: { sku },
  });

  return !existing;
}

// 2. Implement proper image optimization
async function optimizeImage(image: Buffer): Promise<Buffer> {
  // Implement image compression and resizing
  return image;
}

// 3. Use proper SEO meta tags
function generateMetaTags(product: Product): {
  title: string;
  description: string;
  keywords: string[];
} {
  return {
    title: `${product.name} | ${process.env.SITE_NAME}`,
    description: product.shortDescription || product.description?.substring(0, 160),
    keywords: product.seoKeywords || [],
  };
}

// 4. Implement proper category hierarchy
async function getCategoryPath(categoryId: string): Promise<Category[]> {
  const path: Category[] = [];
  let category = await prisma.category.findUnique({
    where: { id: categoryId },
  });

  while (category) {
    path.unshift(category);
    category = category.parentId
      ? await prisma.category.findUnique({ where: { id: category.parentId } })
      : null;
  }

  return path;
}

// 5. Use proper pricing rules
async function applyPricingRules(
  productId: string,
  userId?: string
): Promise<number> {
  const rules = await prisma.pricingRule.findMany({
    where: {
      active: true,
      productIds: { has: productId },
    },
  });

  let maxDiscount = 0;

  for (const rule of rules) {
    if (matchesConditions(rule, userId)) {
      maxDiscount = Math.max(maxDiscount, rule.discount);
    }
  }

  return maxDiscount;
}
```

---

---

## Quick Start

### Product Model

```typescript
interface Product {
  id: string
  name: string
  description: string
  price: number
  variants: ProductVariant[]
  categories: string[]
  tags: string[]
  images: string[]
}

interface ProductVariant {
  id: string
  name: string  // e.g., "Size: Large, Color: Red"
  price: number
  sku: string
  stock: number
  attributes: Record<string, string>  // { size: "L", color: "red" }
}
```

### Product Search

```typescript
async function searchProducts(query: string, filters: Filters) {
  return await db.products.findMany({
    where: {
      AND: [
        {
          OR: [
            { name: { contains: query, mode: 'insensitive' } },
            { description: { contains: query, mode: 'insensitive' } }
          ]
        },
        { categories: { hasSome: filters.categories } },
        { price: { gte: filters.minPrice, lte: filters.maxPrice } }
      ]
    },
    orderBy: { relevance: 'desc' }
  })
}
```

---

## Production Checklist

- [ ] **Product Data Model**: Flexible product data model
- [ ] **Variants**: Support product variants (size, color, etc.)
- [ ] **Categories**: Hierarchical category structure
- [ ] **Search**: Fast full-text search
- [ ] **Filters**: Product filtering and faceting
- [ ] **Images**: Image management and optimization
- [ ] **SEO**: SEO-friendly URLs and metadata
- [ ] **Pricing**: Support pricing rules and discounts
- [ ] **Bulk Operations**: Bulk import/export
- [ ] **Performance**: Optimize for large catalogs
- [ ] **Caching**: Cache product data
- [ ] **Validation**: Validate product data

---

## Anti-patterns

### ❌ Don't: No Variants Support

```typescript
// ❌ Bad - Separate products for variants
const product1 = { name: 'T-Shirt Red Small', price: 20 }
const product2 = { name: 'T-Shirt Red Medium', price: 20 }
// Duplicate data!
```

```typescript
// ✅ Good - Variants
const product = {
  name: 'T-Shirt',
  variants: [
    { size: 'S', color: 'red', price: 20 },
    { size: 'M', color: 'red', price: 20 }
  ]
}
```

### ❌ Don't: Slow Search

```typescript
// ❌ Bad - Full table scan
const products = await db.products.findMany({
  where: { name: { contains: query } }  // No index!
})
```

```typescript
// ✅ Good - Indexed search
// Create index
CREATE INDEX idx_products_name ON products USING gin(to_tsvector('english', name))

// Search with full-text
const products = await db.$queryRaw`
  SELECT * FROM products
  WHERE to_tsvector('english', name) @@ plainto_tsquery(${query})
`
```

---

## Integration Points

- **Shopping Cart** (`30-ecommerce/shopping-cart/`) - Add to cart
- **Inventory Management** (`30-ecommerce/inventory-management/`) - Stock tracking
- **Search** (`20-ai-integration/ai-search/`) - Advanced search

---

## Further Reading

- [Shopify Product API](https://shopify.dev/api/admin-graphql/latest/objects/Product)
- [WooCommerce Products](https://woocommerce.github.io/woocommerce-rest-api-docs/#products)
- [Magento 2 Product API](https://devdocs.magento.com/guides/v2.4/rest/bk-rest.html)
- [BigCommerce Products](https://developer.bigcommerce.com/api-reference/catalog/catalog-api/products)
