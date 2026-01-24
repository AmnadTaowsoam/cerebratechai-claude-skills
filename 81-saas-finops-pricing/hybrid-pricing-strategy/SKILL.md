---
name: Hybrid Pricing Strategy
description: Combining subscription, usage-based, and one-time pricing models to optimize revenue and customer satisfaction
---

# Hybrid Pricing Strategy

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** Business Strategy / Pricing / Product Management
> **Skill ID:** 128

---

## Overview
Hybrid Pricing Strategy combines multiple pricing models (subscription, usage-based, one-time fees) into a cohesive pricing structure. This approach maximizes revenue by capturing value from different customer segments while providing flexibility and predictability for customers.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, customers demand pricing flexibility that matches their usage patterns and budget preferences. Pure subscription models miss revenue from power users, while pure usage-based models create uncertainty for budget-conscious customers. Hybrid models capture the best of both worlds.

### Business Impact
- **Revenue Growth:** 25-45% higher revenue through optimized pricing
- **Customer Acquisition:** 20-30% higher conversion rates with flexible options
- **Customer Retention:** 15-25% lower churn through aligned pricing
- **Market Expansion:** Access to multiple customer segments simultaneously

### Product Thinking
Solves the critical problem where single pricing models leave money on the table by not matching diverse customer needs and usage patterns, resulting in suboptimal revenue capture and customer satisfaction.

## Core Concepts / Technical Deep Dive

### 1. Hybrid Pricing Components

**Base Subscription:**
- Recurring monthly/annual fee
- Provides baseline revenue predictability
- Includes core features and usage allowances

**Usage-Based Overage:**
- Additional charges for usage beyond included allowance
- Captures revenue from power users
- Aligns costs with value received

**One-Time Fees:**
- Setup fees, onboarding costs, implementation fees
- Professional services, training, custom integrations
- Covers upfront costs for complex implementations

**Add-Ons and Upgrades:**
- Additional features, premium support, SLAs
- Advanced capabilities, white-labeling
- Enables upselling and cross-selling

### 2. Pricing Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Customer  │────▶│   Pricing    │────▶│   Revenue   │────▶│   Invoice   │
│   Selection │     │   Engine     │     │   Calculator│     │   Generator │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Plans &   │     │   Usage      │     │   Revenue   │     │   Payment   │
│   Tiers     │     │   Metering   │     │   Streams   │     │   Gateway   │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

### 3. Pricing Strategy Patterns

**Freemium + Subscription:**
- Free tier with limited features/usage
- Paid tiers with more features/usage
- Lowers barrier to entry

**Subscription + Usage:**
- Base subscription for predictable revenue
- Usage overage for variable revenue
- Best balance of predictability and value capture

**Tiered + Volume Discounts:**
- Multiple subscription tiers
- Volume discounts for large customers
- Serves SMB to enterprise segments

**Commitment + Flexibility:**
- Annual commitments with discounts
- Monthly flexibility with premium
- Captures different customer preferences

### 4. Pricing Optimization

**Customer Segmentation:**
- SMB: Lower price points, self-service
- Mid-market: Balanced pricing, some support
- Enterprise: Custom pricing, dedicated support

**Value-Based Pricing:**
- Price based on customer value received
- Different pricing for different use cases
- Captures more value from high-value customers

**Competitive Positioning:**
- Price leadership: Lowest prices
- Value-based: Premium pricing for differentiation
- Competitive: Match or beat competitors

**A/B Testing:**
- Test different price points
- Measure conversion and revenue impact
- Continuously optimize pricing

## Tooling & Tech Stack

### Enterprise Tools
- **Stripe Billing:** Hybrid pricing with subscriptions and usage
- **Chargebee:** Multi-model billing platform
- **Zuora:** Enterprise subscription and usage billing
- **Recurly:** Flexible billing platform
- **Pricelabs:** Pricing optimization and analytics
- **ProfitWell:** Revenue analytics and pricing insights

### Configuration Essentials

```yaml
# Hybrid pricing configuration
pricing_strategy:
  # Base subscription tiers
  subscription_tiers:
    - name: "starter"
      monthly_price: 49.0
      annual_price: 490.0  # ~17% discount
      annual_discount: 0.17
      included_usage:
        api_calls: 10000
        storage_gb: 10
        users: 5
      features: ["basic_analytics", "email_support"]
    
    - name: "professional"
      monthly_price: 199.0
      annual_price: 1990.0
      annual_discount: 0.17
      included_usage:
        api_calls: 100000
        storage_gb: 100
        users: 25
      features: ["advanced_analytics", "priority_support", "api_access"]
    
    - name: "enterprise"
      monthly_price: 999.0
      annual_price: 9990.0
      annual_discount: 0.17
      included_usage:
        api_calls: 1000000
        storage_gb: 1000
        users: 100
      features: ["custom_analytics", "dedicated_support", "sla", "sso"]
  
  # Usage-based overage pricing
  overage_pricing:
    api_calls:
      unit_price: 0.001
      tier_discounts:
        - threshold: 1000000
          discount_percent: 10
        - threshold: 10000000
          discount_percent: 20
    
    storage_gb:
      unit_price: 0.10
      tier_discounts:
        - threshold: 1000
          discount_percent: 15
        - threshold: 10000
          discount_percent: 25
  
  # One-time fees
  one_time_fees:
    setup_fee: 500.0
    onboarding_fee: 1000.0
    implementation_fee: 5000.0
    training_fee: 500.0
  
  # Add-ons
  add_ons:
    - name: "premium_support"
      monthly_price: 99.0
      features: ["24_7_support", "dedicated_account_manager"]
    
    - name: "white_label"
      monthly_price: 299.0
      features: ["custom_branding", "custom_domain"]
    
    - name: "advanced_analytics"
      monthly_price: 199.0
      features: ["custom_reports", "data_export", "api_analytics"]
  
  # Commitment discounts
  commitment_discounts:
    - commitment_months: 12
      discount_percent: 17
    - commitment_months: 24
      discount_percent: 25
    - commitment_months: 36
      discount_percent: 30
```

## Code Examples

### Good vs Bad Examples

```python
# ❌ Bad - Single pricing model, no flexibility
def calculate_price(customer_id):
    # All customers pay the same
    return 100.0

# ✅ Good - Hybrid pricing with multiple components
def calculate_hybrid_price(customer_id, usage, plan):
    # Base subscription
    base_price = plan['monthly_price']
    
    # Usage overage
    overage = calculate_overage(usage, plan['included_usage'])
    overage_price = overage * plan['overage_rate']
    
    # Add-ons
    add_on_price = sum(add_on['price'] for add_on in customer['add_ons'])
    
    # Commitment discount
    discount = calculate_commitment_discount(customer_id['commitment_months'])
    
    total_price = (base_price + overage_price + add_on_price) * (1 - discount)
    return total_price
```

```python
# ❌ Bad - No annual discount, no incentive for commitment
def get_price(plan_type, billing_cycle):
    return base_prices[plan_type]

# ✅ Good - Annual discounts and commitment incentives
def get_price(plan_type, billing_cycle, commitment_months=None):
    base_price = base_prices[plan_type]
    
    # Apply annual discount
    if billing_cycle == 'annual':
        base_price *= 0.83  # 17% discount
    
    # Apply commitment discount
    if commitment_months:
        discount = get_commitment_discount(commitment_months)
        base_price *= (1 - discount)
    
    return base_price
```

### Implementation Example

```python
"""
Production-ready Hybrid Pricing Engine
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BillingCycle(Enum):
    """Billing cycle options."""
    MONTHLY = "monthly"
    ANNUAL = "annual"
    QUARTERLY = "quarterly"


class PlanType(Enum):
    """Plan types."""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


@dataclass
class SubscriptionTier:
    """Subscription tier definition."""
    name: PlanType
    monthly_price: float
    annual_price: float
    annual_discount: float
    included_usage: Dict[str, float]
    features: List[str]


@dataclass
class OveragePricing:
    """Usage overage pricing."""
    metric_name: str
    unit_price: float
    tier_discounts: List[Tuple[float, float]]  # (threshold, discount_percent)


@dataclass
class AddOn:
    """Add-on product."""
    name: str
    monthly_price: float
    features: List[str]


@dataclass
class CommitmentDiscount:
    """Commitment discount tier."""
    months: int
    discount_percent: float


@dataclass
class OneTimeFee:
    """One-time fee."""
    name: str
    amount: float
    description: str


@dataclass
class Customer:
    """Customer information."""
    customer_id: str
    plan_type: PlanType
    billing_cycle: BillingCycle
    commitment_months: Optional[int] = None
    add_ons: List[str] = field(default_factory=list)
    usage: Dict[str, float] = field(default_factory=dict)
    one_time_fees: List[str] = field(default_factory=list)


@dataclass
class Invoice:
    """Invoice for a customer."""
    customer_id: str
    billing_period_start: datetime
    billing_period_end: datetime
    charges: Dict[str, float]
    discounts: Dict[str, float]
    subtotal: float
    total_amount: float
    currency: str


class HybridPricingEngine:
    """
    Enterprise-grade hybrid pricing engine.
    """
    
    def __init__(
        self,
        subscription_tiers: List[SubscriptionTier],
        overage_pricing: List[OveragePricing],
        add_ons: List[AddOn],
        commitment_discounts: List[CommitmentDiscount],
        one_time_fees: List[OneTimeFee]
    ):
        """
        Initialize hybrid pricing engine.
        
        Args:
            subscription_tiers: List of subscription tiers
            overage_pricing: List of overage pricing rules
            add_ons: List of available add-ons
            commitment_discounts: List of commitment discount tiers
            one_time_fees: List of one-time fees
        """
        self.subscription_tiers = {t.name: t for t in subscription_tiers}
        self.overage_pricing = {p.metric_name: p for p in overage_pricing}
        self.add_ons = {a.name: a for a in add_ons}
        self.commitment_discounts = sorted(commitment_discounts, key=lambda d: d.months)
        self.one_time_fees = {f.name: f for f in one_time_fees}
        
        logger.info(f"Hybrid pricing engine initialized with {len(subscription_tiers)} tiers")
    
    def calculate_base_subscription_price(
        self,
        plan_type: PlanType,
        billing_cycle: BillingCycle,
        commitment_months: Optional[int] = None
    ) -> Tuple[float, float]:
        """
        Calculate base subscription price.
        
        Args:
            plan_type: Type of plan
            billing_cycle: Billing cycle
            commitment_months: Optional commitment period
            
        Returns:
            Tuple of (base_price, total_discount)
        """
        tier = self.subscription_tiers[plan_type]
        
        # Get base price based on billing cycle
        if billing_cycle == BillingCycle.ANNUAL:
            base_price = tier.annual_price / 12  # Monthly equivalent
            annual_discount = tier.annual_discount
        else:
            base_price = tier.monthly_price
            annual_discount = 0.0
        
        total_discount = annual_discount
        
        # Apply commitment discount
        if commitment_months:
            commitment_discount = self._get_commitment_discount(commitment_months)
            total_discount += commitment_discount
        
        # Calculate final price
        final_price = base_price * (1 - total_discount)
        
        logger.debug(
            f"Base price for {plan_type.value}: "
            f"${base_price:.2f} - {total_discount*100:.1f}% = ${final_price:.2f}"
        )
        
        return final_price, total_discount
    
    def _get_commitment_discount(self, months: int) -> float:
        """
        Get commitment discount for a given period.
        
        Args:
            months: Commitment period in months
            
        Returns:
            Discount percentage (0-1)
        """
        for discount in reversed(self.commitment_discounts):
            if months >= discount.months:
                return discount.discount_percent / 100
        return 0.0
    
    def calculate_overage_price(
        self,
        usage: Dict[str, float],
        plan_type: PlanType
    ) -> float:
        """
        Calculate usage overage price.
        
        Args:
            usage: Actual usage metrics
            plan_type: Type of plan
            
        Returns:
            Total overage price
        """
        tier = self.subscription_tiers[plan_type]
        total_overage = 0.0
        
        for metric_name, actual_usage in usage.items():
            # Get included usage
            included_usage = tier.included_usage.get(metric_name, 0)
            
            # Calculate overage
            overage = max(0, actual_usage - included_usage)
            
            if overage > 0 and metric_name in self.overage_pricing:
                pricing = self.overage_pricing[metric_name]
                
                # Calculate base overage price
                base_price = overage * pricing.unit_price
                
                # Apply tier discounts
                discount = self._get_overage_discount(pricing, actual_usage)
                final_price = base_price * (1 - discount)
                
                total_overage += final_price
                
                logger.debug(
                    f"Overage for {metric_name}: {overage} × ${pricing.unit_price} "
                    f"× {(1-discount)*100:.0f}% = ${final_price:.2f}"
                )
        
        return total_overage
    
    def _get_overage_discount(
        self,
        pricing: OveragePricing,
        usage: float
    ) -> float:
        """
        Get overage discount based on usage volume.
        
        Args:
            pricing: Overage pricing configuration
            usage: Total usage
            
        Returns:
            Discount percentage (0-1)
        """
        for threshold, discount in reversed(pricing.tier_discounts):
            if usage >= threshold:
                return discount / 100
        return 0.0
    
    def calculate_add_on_price(self, add_on_names: List[str]) -> float:
        """
        Calculate total add-on price.
        
        Args:
            add_on_names: List of add-on names
            
        Returns:
            Total add-on price
        """
        total_price = 0.0
        
        for name in add_on_names:
            if name in self.add_ons:
                total_price += self.add_ons[name].monthly_price
                logger.debug(f"Add-on {name}: ${self.add_ons[name].monthly_price:.2f}")
        
        return total_price
    
    def calculate_one_time_fees(self, fee_names: List[str]) -> float:
        """
        Calculate total one-time fees.
        
        Args:
            fee_names: List of fee names
            
        Returns:
            Total one-time fees
        """
        total_fees = 0.0
        
        for name in fee_names:
            if name in self.one_time_fees:
                total_fees += self.one_time_fees[name].amount
                logger.debug(f"One-time fee {name}: ${self.one_time_fees[name].amount:.2f}")
        
        return total_fees
    
    def calculate_invoice(
        self,
        customer: Customer,
        billing_period_start: datetime,
        billing_period_end: datetime,
        include_one_time_fees: bool = False
    ) -> Invoice:
        """
        Calculate complete invoice for a customer.
        
        Args:
            customer: Customer information
            billing_period_start: Start of billing period
            billing_period_end: End of billing period
            include_one_time_fees: Whether to include one-time fees
            
        Returns:
            Invoice object
        """
        charges = {}
        discounts = {}
        
        # Calculate base subscription price
        base_price, subscription_discount = self.calculate_base_subscription_price(
            customer.plan_type,
            customer.billing_cycle,
            customer.commitment_months
        )
        charges['subscription'] = base_price
        if subscription_discount > 0:
            discounts['annual_discount'] = subscription_discount
        
        # Calculate overage price
        overage_price = self.calculate_overage_price(
            customer.usage,
            customer.plan_type
        )
        if overage_price > 0:
            charges['usage_overage'] = overage_price
        
        # Calculate add-on price
        add_on_price = self.calculate_add_on_price(customer.add_ons)
        if add_on_price > 0:
            charges['add_ons'] = add_on_price
        
        # Calculate one-time fees
        if include_one_time_fees and customer.one_time_fees:
            one_time_price = self.calculate_one_time_fees(customer.one_time_fees)
            if one_time_price > 0:
                charges['one_time_fees'] = one_time_price
        
        # Calculate subtotal and total
        subtotal = sum(charges.values())
        total_discount = sum(discounts.values())
        total_amount = subtotal - (subtotal * total_discount)
        
        # Create invoice
        invoice = Invoice(
            customer_id=customer.customer_id,
            billing_period_start=billing_period_start,
            billing_period_end=billing_period_end,
            charges=charges,
            discounts=discounts,
            subtotal=subtotal,
            total_amount=total_amount,
            currency="USD"
        )
        
        logger.info(
            f"Invoice generated for {customer.customer_id}: "
            f"${total_amount:.2f} ({customer.plan_type.value}, {customer.billing_cycle.value})"
        )
        
        return invoice
    
    def estimate_price(
        self,
        plan_type: PlanType,
        billing_cycle: BillingCycle,
        projected_usage: Dict[str, float],
        add_ons: List[str] = None,
        commitment_months: Optional[int] = None
    ) -> float:
        """
        Estimate price based on projected usage.
        
        Args:
            plan_type: Type of plan
            billing_cycle: Billing cycle
            projected_usage: Projected usage metrics
            add_ons: List of add-ons
            commitment_months: Optional commitment period
            
        Returns:
            Estimated monthly price
        """
        # Create temporary customer
        customer = Customer(
            customer_id="estimate",
            plan_type=plan_type,
            billing_cycle=billing_cycle,
            commitment_months=commitment_months,
            add_ons=add_ons or [],
            usage=projected_usage
        )
        
        # Calculate invoice
        invoice = self.calculate_invoice(
            customer,
            datetime.utcnow(),
            datetime.utcnow() + timedelta(days=30)
        )
        
        return invoice.total_amount


# Example usage
if __name__ == "__main__":
    # Define subscription tiers
    tiers = [
        SubscriptionTier(
            name=PlanType.STARTER,
            monthly_price=49.0,
            annual_price=490.0,
            annual_discount=0.17,
            included_usage={
                'api_calls': 10000,
                'storage_gb': 10,
                'users': 5
            },
            features=["basic_analytics", "email_support"]
        ),
        SubscriptionTier(
            name=PlanType.PROFESSIONAL,
            monthly_price=199.0,
            annual_price=1990.0,
            annual_discount=0.17,
            included_usage={
                'api_calls': 100000,
                'storage_gb': 100,
                'users': 25
            },
            features=["advanced_analytics", "priority_support", "api_access"]
        )
    ]
    
    # Define overage pricing
    overage = [
        OveragePricing(
            metric_name='api_calls',
            unit_price=0.001,
            tier_discounts=[
                (1000000, 10),
                (10000000, 20)
            ]
        ),
        OveragePricing(
            metric_name='storage_gb',
            unit_price=0.10,
            tier_discounts=[
                (1000, 15),
                (10000, 25)
            ]
        )
    ]
    
    # Define add-ons
    add_ons = [
        AddOn(
            name="premium_support",
            monthly_price=99.0,
            features=["24_7_support", "dedicated_account_manager"]
        ),
        AddOn(
            name="advanced_analytics",
            monthly_price=199.0,
            features=["custom_reports", "data_export"]
        )
    ]
    
    # Define commitment discounts
    commitment_discounts = [
        CommitmentDiscount(months=12, discount_percent=17),
        CommitmentDiscount(months=24, discount_percent=25),
        CommitmentDiscount(months=36, discount_percent=30)
    ]
    
    # Define one-time fees
    one_time_fees = [
        OneTimeFee(name="setup", amount=500.0, description="Initial setup"),
        OneTimeFee(name="onboarding", amount=1000.0, description="Onboarding assistance")
    ]
    
    # Create pricing engine
    engine = HybridPricingEngine(
        subscription_tiers=tiers,
        overage_pricing=overage,
        add_ons=add_ons,
        commitment_discounts=commitment_discounts,
        one_time_fees=one_time_fees
    )
    
    # Create customer
    customer = Customer(
        customer_id="cust_001",
        plan_type=PlanType.PROFESSIONAL,
        billing_cycle=BillingCycle.ANNUAL,
        commitment_months=12,
        add_ons=["premium_support"],
        usage={
            'api_calls': 150000,
            'storage_gb': 150
        },
        one_time_fees=["setup"]
    )
    
    # Calculate invoice
    invoice = engine.calculate_invoice(
        customer,
        datetime(2025, 1, 1),
        datetime(2025, 1, 31),
        include_one_time_fees=True
    )
    
    print(f"\nInvoice for {customer.customer_id}:")
    print(f"  Plan: {customer.plan_type.value}")
    print(f"  Billing Cycle: {customer.billing_cycle.value}")
    print(f"  Total Amount: ${invoice.total_amount:.2f}")
    print(f"\n  Charges:")
    for charge_name, amount in invoice.charges.items():
        print(f"    {charge_name}: ${amount:.2f}")
    print(f"\n  Discounts:")
    for discount_name, discount in invoice.discounts.items():
        print(f"    {discount_name}: {discount*100:.1f}%")
    
    # Estimate price for different scenarios
    print(f"\nPrice Estimates:")
    
    # Monthly, no commitment
    estimate1 = engine.estimate_price(
        plan_type=PlanType.STARTER,
        billing_cycle=BillingCycle.MONTHLY,
        projected_usage={'api_calls': 50000, 'storage_gb': 50}
    )
    print(f"  Monthly Starter: ${estimate1:.2f}")
    
    # Annual, 12-month commitment
    estimate2 = engine.estimate_price(
        plan_type=PlanType.PROFESSIONAL,
        billing_cycle=BillingCycle.ANNUAL,
        projected_usage={'api_calls': 150000, 'storage_gb': 150},
        commitment_months=12
    )
    print(f"  Annual Professional (12mo): ${estimate2:.2f}")
    
    # Annual, 24-month commitment
    estimate3 = engine.estimate_price(
        plan_type=PlanType.PROFESSIONAL,
        billing_cycle=BillingCycle.ANNUAL,
        projected_usage={'api_calls': 150000, 'storage_gb': 150},
        commitment_months=24
    )
    print(f"  Annual Professional (24mo): ${estimate3:.2f}")
```

## Standards, Compliance & Security

### International Standards
- **ASC 606:** Revenue recognition for hybrid pricing
- **IFRS 15:** International revenue recognition
- **PCI DSS:** Security for payment processing
- **SOC 2 Type II:** Security and availability of billing systems

### Security Protocol
- **Data Encryption:** Encrypt billing and customer data
- **Access Control:** Role-based access to pricing information
- **Audit Logging:** Complete audit trail of pricing changes
- **Fraud Detection:** Monitor for unusual billing patterns

### Explainability
- **Transparent Pricing:** Clear documentation of all charges
- **Invoice Clarity:** Detailed breakdown of charges and discounts
- **Usage Visibility:** Real-time usage dashboards for customers

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install pandas numpy stripe
   ```

2. **Define pricing components:**
   ```python
   engine = HybridPricingEngine(
       subscription_tiers=tiers,
       overage_pricing=overage,
       add_ons=add_ons
   )
   ```

3. **Calculate invoice:**
   ```python
   invoice = engine.calculate_invoice(customer, start_date, end_date)
   print(f"Total: ${invoice.total_amount:.2f}")
   ```

4. **Estimate pricing:**
   ```python
   estimated = engine.estimate_price(
       plan_type=PlanType.PROFESSIONAL,
       billing_cycle=BillingCycle.ANNUAL,
       projected_usage={'api_calls': 100000}
   )
   ```

## Production Checklist

- [ ] Subscription tiers defined and documented
- [ ] Usage-based overage pricing configured
- [ ] Add-ons and upgrades available
- [ ] One-time fees defined
- [ ] Commitment discounts configured
- [ ] Annual discounts implemented
- [ ] Billing integration set up
- [ ] Invoice generation automated
- [ ] Pricing strategy reviewed quarterly
- [ ] A/B testing for pricing changes

## Anti-patterns

1. **Over-complex Pricing:** Too many options confuse customers
   - **Why it's bad:** Lower conversion, higher support costs
   - **Solution:** Limit to 3-5 pricing tiers

2. **Hidden Fees:** Not clearly communicating all charges
   - **Why it's bad:** Customer distrust, churn
   - **Solution:** Transparent pricing with clear documentation

3. **No Upsell Path:** No clear path for customers to upgrade
   - **Why it's bad:** Missed revenue opportunities
   - **Solution:** Clear upgrade paths and in-app prompts

4. **Rigid Pricing:** Cannot adapt to market changes
   - **Why it's bad:** Lost competitive advantage
   - **Solution:** Configurable pricing engine

## Unit Economics & KPIs

### Cost Calculation
```
Revenue per Customer = Base Subscription + Usage Overage + Add-Ons

Gross Margin = (Revenue - COGS) / Revenue

Customer LTV = Average Monthly Profit × Customer Lifetime

Price Elasticity = % Change in Demand / % Change in Price
```

### Key Performance Indicators
- **Conversion Rate:** > 15% for free to paid
- **ARPU Growth:** > 15% year-over-year
- **Churn Rate:** < 5% monthly
- **Revenue per Tier:** Track revenue by pricing tier
- **Add-On Adoption:** > 20% of customers purchase add-ons

## Integration Points / Related Skills
- [Cloud Unit Economics](../81-saas-finops-pricing/cloud-unit-economics/SKILL.md) - For calculating COGS
- [Usage Based Pricing](../81-saas-finops-pricing/usage-based-pricing/SKILL.md) - For usage-based components
- [Billing System Architecture](../81-saas-finops-pricing/billing-system-architecture/SKILL.md) - For billing infrastructure
- [Customer Lifetime Value](../81-saas-finops-pricing/customer-lifetime-value/SKILL.md) - For LTV calculations

## Further Reading
- [Stripe Billing Documentation](https://stripe.com/docs/billing)
- [Hybrid Pricing Strategy](https://www.priceintelligently.com/blog/hybrid-pricing)
- [SaaS Pricing Guide](https://www.saastr.com/2020/01/10-key-saas-metrics-startups-need-to-track/)
- [Pricing Psychology](https://hbr.org/2019/03/the-psychology-of-pricing)
- [Revenue Recognition ASC 606](https://www.fasb.org/jsp/FASB/Page/SectionPage&cid=1176157312633)
