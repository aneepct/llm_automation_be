# Horys Mall Database Schema

> Auto-generated from `horysmall_schema.sql` (pgAdmin ERD export)
> 
> **121 tables** · **149 foreign keys** · PostgreSQL · camelCase columns

---

## Overview

| Item | Value |
|------|-------|
| Tables | 121 |
| Foreign keys | 149 |
| Customer ID | `users.bid` |
| Order public ID | `orders.orderId` |
| User ↔ order link | `orders.userBID` = `users.bid` (no FK) |

---

## Table of contents

- [Admin](#admin) (7 tables)
- [Cart & checkout](#cart--checkout) (5 tables)
- [Catalog](#catalog) (14 tables)
- [Extension carts](#extension-carts) (6 tables)
- [Geography](#geography) (2 tables)
- [Legacy orders](#legacy-orders) (2 tables)
- [Migration & gen2](#migration--gen2) (9 tables)
- [Migration carts](#migration-carts) (6 tables)
- [Migrations metadata](#migrations-metadata) (1 tables)
- [Orders](#orders) (10 tables)
- [Other](#other) (6 tables)
- [Payments](#payments) (6 tables)
- [Queues & jobs](#queues--jobs) (9 tables)
- [Shipping & fulfillment](#shipping--fulfillment) (15 tables)
- [Shipping carts](#shipping-carts) (6 tables)
- [System & misc](#system--misc) (8 tables)
- [Upgrade carts](#upgrade-carts) (6 tables)
- [Users & addresses](#users--addresses) (3 tables)
- [All tables (detailed)](#all-tables-detailed)
- [Foreign keys](#foreign-keys)
- [Support query patterns](#support-query-patterns)

---

## Admin

| Table | Columns |
|-------|---------|
| [`admin_activities`](#table-admin-activities) | 10 |
| [`admin_export_jobs`](#table-admin-export-jobs) | 17 |
| [`admin_features`](#table-admin-features) | 8 |
| [`admin_modules`](#table-admin-modules) | 7 |
| [`admin_role_access`](#table-admin-role-access) | 7 |
| [`admin_roles`](#table-admin-roles) | 7 |
| [`admins`](#table-admins) | 12 |

---

## Cart & checkout

| Table | Columns |
|-------|---------|
| [`cart_assets`](#table-cart-assets) | 14 |
| [`cart_fees`](#table-cart-fees) | 7 |
| [`cart_products`](#table-cart-products) | 22 |
| [`cart_taxes`](#table-cart-taxes) | 7 |
| [`carts`](#table-carts) | 21 |

---

## Catalog

| Table | Columns |
|-------|---------|
| [`categories`](#table-categories) | 12 |
| [`product_eligibility_criterias`](#table-product-eligibility-criterias) | 10 |
| [`product_extension_configurations`](#table-product-extension-configurations) | 11 |
| [`product_files`](#table-product-files) | 8 |
| [`product_images`](#table-product-images) | 2 |
| [`product_shipment_configurations`](#table-product-shipment-configurations) | 7 |
| [`product_shipping_cashback_assets`](#table-product-shipping-cashback-assets) | 12 |
| [`product_shipping_costs`](#table-product-shipping-costs) | 8 |
| [`product_tags`](#table-product-tags) | 2 |
| [`product_upgrades`](#table-product-upgrades) | 15 |
| [`products`](#table-products) | 32 |
| [`stores`](#table-stores) | 13 |
| [`subproducts`](#table-subproducts) | 13 |
| [`tags`](#table-tags) | 7 |

---

## Extension carts

| Table | Columns |
|-------|---------|
| [`extension_cart_assets`](#table-extension-cart-assets) | 14 |
| [`extension_cart_cashbacks`](#table-extension-cart-cashbacks) | 6 |
| [`extension_cart_fees`](#table-extension-cart-fees) | 7 |
| [`extension_cart_products`](#table-extension-cart-products) | 21 |
| [`extension_cart_taxes`](#table-extension-cart-taxes) | 7 |
| [`extension_carts`](#table-extension-carts) | 25 |

---

## Geography

| Table | Columns |
|-------|---------|
| [`country_cities`](#table-country-cities) | 9 |
| [`country_states`](#table-country-states) | 9 |

---

## Legacy orders

| Table | Columns |
|-------|---------|
| [`legacy_order_items`](#table-legacy-order-items) | 23 |
| [`legacy_orders`](#table-legacy-orders) | 31 |

---

## Migration & gen2

| Table | Columns |
|-------|---------|
| [`_prisma_migrations`](#table--prisma-migrations) | 8 |
| [`gen2_gen3_orders_migration_map`](#table-gen2-gen3-orders-migration-map) | 5 |
| [`gen2_migration_eligibility_v2`](#table-gen2-migration-eligibility-v2) | 16 |
| [`gen2_migration_queue_items`](#table-gen2-migration-queue-items) | 14 |
| [`gen2_shipment_migration_config`](#table-gen2-shipment-migration-config) | 13 |
| [`migration_refund_request_items`](#table-migration-refund-request-items) | 7 |
| [`migration_refund_requests`](#table-migration-refund-requests) | 13 |
| [`migrations`](#table-migrations) | 3 |
| [`typeORM_migrations`](#table-typeORM-migrations) | 3 |

---

## Migration carts

| Table | Columns |
|-------|---------|
| [`migration_cart_assets`](#table-migration-cart-assets) | 14 |
| [`migration_cart_cashbacks`](#table-migration-cart-cashbacks) | 6 |
| [`migration_cart_fees`](#table-migration-cart-fees) | 7 |
| [`migration_cart_products`](#table-migration-cart-products) | 22 |
| [`migration_cart_taxes`](#table-migration-cart-taxes) | 7 |
| [`migration_carts`](#table-migration-carts) | 26 |

---

## Migrations metadata

| Table | Columns |
|-------|---------|
| [`typeorm_metadata`](#table-typeorm-metadata) | 6 |

---

## Orders

| Table | Columns |
|-------|---------|
| [`order_invoices`](#table-order-invoices) | 6 |
| [`order_item_units`](#table-order-item-units) | 13 |
| [`order_items`](#table-order-items) | 30 |
| [`order_items_v1`](#table-order-items-v1) | 21 |
| [`order_shipping_address_histories`](#table-order-shipping-address-histories) | 13 |
| [`order_transaction_v1`](#table-order-transaction-v1) | 14 |
| [`order_transactions`](#table-order-transactions) | 14 |
| [`order_unit_extension_eligibilities`](#table-order-unit-extension-eligibilities) | 15 |
| [`orders`](#table-orders) | 55 |
| [`orders_v1`](#table-orders-v1) | 35 |

---

## Other

| Table | Columns |
|-------|---------|
| [`card_sequence_number`](#table-card-sequence-number) | 4 |
| [`legacy_shipment_items`](#table-legacy-shipment-items) | 13 |
| [`legacy_shipment_status_update_queue_items`](#table-legacy-shipment-status-update-queue-items) | 19 |
| [`machine_extension_queue_items`](#table-machine-extension-queue-items) | 17 |
| [`upgradable_items`](#table-upgradable-items) | 13 |
| [`wallet_sequence_number`](#table-wallet-sequence-number) | 4 |

---

## Payments

| Table | Columns |
|-------|---------|
| [`payment_assets`](#table-payment-assets) | 10 |
| [`payment_callbacks`](#table-payment-callbacks) | 10 |
| [`payment_fees`](#table-payment-fees) | 11 |
| [`payment_methods`](#table-payment-methods) | 16 |
| [`payment_options`](#table-payment-options) | 18 |
| [`payment_restrictions`](#table-payment-restrictions) | 10 |

---

## Queues & jobs

| Table | Columns |
|-------|---------|
| [`connect_queue_item`](#table-connect-queue-item) | 8 |
| [`ioss_queue_item`](#table-ioss-queue-item) | 8 |
| [`machine_upgrade_queue_item`](#table-machine-upgrade-queue-item) | 9 |
| [`partner_hub_bulk_address_verify_job_items`](#table-partner-hub-bulk-address-verify-job-items) | 8 |
| [`partner_hub_bulk_address_verify_jobs`](#table-partner-hub-bulk-address-verify-jobs) | 13 |
| [`partner_hub_order_address_sync_logs`](#table-partner-hub-order-address-sync-logs) | 8 |
| [`queue_partner_hub_orders`](#table-queue-partner-hub-orders) | 8 |
| [`sync_service_queue_item`](#table-sync-service-queue-item) | 8 |
| [`xera_queue_item`](#table-xera-queue-item) | 8 |

---

## Shipping & fulfillment

| Table | Columns |
|-------|---------|
| [`shipment_item_logs`](#table-shipment-item-logs) | 10 |
| [`shipment_items`](#table-shipment-items) | 19 |
| [`shipment_order_invoices`](#table-shipment-order-invoices) | 6 |
| [`shipment_order_items`](#table-shipment-order-items) | 14 |
| [`shipment_order_transactions`](#table-shipment-order-transactions) | 14 |
| [`shipment_orders`](#table-shipment-orders) | 40 |
| [`shipment_status_update_queue_item`](#table-shipment-status-update-queue-item) | 18 |
| [`shipment_webhook_logs`](#table-shipment-webhook-logs) | 16 |
| [`shipping_cashback_assets`](#table-shipping-cashback-assets) | 10 |
| [`shipping_cashback_queue_item`](#table-shipping-cashback-queue-item) | 12 |
| [`shipping_methods`](#table-shipping-methods) | 10 |
| [`shipping_providers`](#table-shipping-providers) | 8 |
| [`shipping_repayment_config`](#table-shipping-repayment-config) | 7 |
| [`shipping_repayment_country_costs`](#table-shipping-repayment-country-costs) | 6 |
| [`shipping_repayment_eligibility`](#table-shipping-repayment-eligibility) | 6 |

---

## Shipping carts

| Table | Columns |
|-------|---------|
| [`shipping_cart_assets`](#table-shipping-cart-assets) | 14 |
| [`shipping_cart_cashbacks`](#table-shipping-cart-cashbacks) | 6 |
| [`shipping_cart_fees`](#table-shipping-cart-fees) | 7 |
| [`shipping_cart_products`](#table-shipping-cart-products) | 13 |
| [`shipping_cart_taxes`](#table-shipping-cart-taxes) | 7 |
| [`shipping_carts`](#table-shipping-carts) | 20 |

---

## System & misc

| Table | Columns |
|-------|---------|
| [`boost_logs`](#table-boost-logs) | 7 |
| [`countries`](#table-countries) | 16 |
| [`credit_notes`](#table-credit-notes) | 9 |
| [`devices`](#table-devices) | 16 |
| [`email_histories`](#table-email-histories) | 12 |
| [`feature_flags`](#table-feature-flags) | 6 |
| [`send_gen_histories`](#table-send-gen-histories) | 9 |
| [`taxes`](#table-taxes) | 11 |

---

## Upgrade carts

| Table | Columns |
|-------|---------|
| [`upgrade_cart_assets`](#table-upgrade-cart-assets) | 14 |
| [`upgrade_cart_cashbacks`](#table-upgrade-cart-cashbacks) | 6 |
| [`upgrade_cart_fees`](#table-upgrade-cart-fees) | 7 |
| [`upgrade_cart_products`](#table-upgrade-cart-products) | 19 |
| [`upgrade_cart_taxes`](#table-upgrade-cart-taxes) | 7 |
| [`upgrade_carts`](#table-upgrade-carts) | 26 |

---

## Users & addresses

| Table | Columns |
|-------|---------|
| [`user_addresses`](#table-user-addresses) | 22 |
| [`user_payment_method_consents`](#table-user-payment-method-consents) | 7 |
| [`users`](#table-users) | 29 |

---

## All tables (detailed)

### `_prisma_migrations` {#table--prisma-migrations}

| Column | Type |
|--------|------|
| `id` | character varying(36) |
| `checksum` | character varying(64) |
| `finished_at` | timestamp with time zone |
| `migration_name` | character varying(255) |
| `logs` | text |
| `rolled_back_at` | timestamp with time zone |
| `started_at` | timestamp with time zone |
| `applied_steps_count` | integer |

### `admin_activities` {#table-admin-activities}

| Column | Type |
|--------|------|
| `id` | serial |
| `adminId` | integer |
| `action` | text |
| `method` | text |
| `data` | text |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `others` | text |

**Foreign keys:**
- `adminId` → `admins.id`

### `admin_export_jobs` {#table-admin-export-jobs}

| Column | Type |
|--------|------|
| `id` | serial |
| `status` | admin_export_job_status_enum |
| `exportDomain` | admin_export_domain_enum |
| `exportType` | admin_export_type_enum |
| `filters` | jsonb |
| `fields` | jsonb |
| `totalCount` | integer |
| `processedCount` | integer |
| `minioObjectKey` | character varying |
| `fileName` | character varying |
| `fileExpiresAt` | timestamp with time zone |
| `createdByAdminId` | integer |
| `createdByAdminEmail` | character varying |
| `errorMessage` | text |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `completedAt` | timestamp with time zone |

### `admin_features` {#table-admin-features}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | text |
| `code` | text |
| `moduleId` | integer |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `moduleId` → `admin_modules.id`

### `admin_modules` {#table-admin-modules}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | text |
| `code` | text |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

### `admin_role_access` {#table-admin-role-access}

| Column | Type |
|--------|------|
| `id` | serial |
| `roleId` | integer |
| `featureId` | integer |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `featureId` → `admin_features.id`
- `roleId` → `admin_roles.id`

### `admin_roles` {#table-admin-roles}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | text |
| `details` | text |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

### `admins` {#table-admins}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | text |
| `userName` | text |
| `email` | text |
| `phone` | text |
| `password` | text |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `roleId` | integer |
| `isSuperAdmin` | boolean |

**Foreign keys:**
- `roleId` → `admin_roles.id`

### `boost_logs` {#table-boost-logs}

| Column | Type |
|--------|------|
| `id` | serial |
| `type` | character varying(50) |
| `payload` | jsonb |
| `error` | jsonb |
| `source` | character varying(100) |
| `statusCode` | integer |
| `createdAt` | timestamp without time zone |

### `card_sequence_number` {#table-card-sequence-number}

| Column | Type |
|--------|------|
| `id` | serial |
| `createdFor` | character varying |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

### `cart_assets` {#table-cart-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `assetOption` | jsonb |
| `calculatedCommision` | jsonb |
| `baseAssetName` | character varying |
| `baseAssetSymbol` | character varying |
| `baseAssetAmount` | numeric |
| `baseAssetPercentage` | numeric |
| `optionAssetName` | character varying |
| `optionAssetSymbol` | character varying |
| `optionAssetAmount` | numeric |
| `optionAssetPercentage` | numeric |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `cartId` → `carts.id`

### `cart_fees` {#table-cart-fees}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `feeName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | cart_fees_type_enum |
| `feeCategory` | cart_fees_feecategory_enum |

**Foreign keys:**
- `cartId` → `carts.id`

### `cart_products` {#table-cart-products}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `productId` | integer |
| `quantity` | integer |
| `canProductBeRemoved` | boolean |
| `feedBackMessage` | character varying |
| `userPurchaseLimit` | integer |
| `canUserPurchaseTheProduct` | boolean |
| `totalOrderExistsForProduct` | integer |
| `maximumUserCanPurchase` | integer |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `price` | numeric |
| `isEligibleForCommission` | boolean |
| `commission` | jsonb |
| `pricePercentage` | numeric |
| `originalPrice` | numeric |
| `utilityToken` | numeric |
| `estimatedDelivery` | numeric |
| `maxCartQuantity` | integer |
| `minCartQuantity` | integer |
| `eligibleMembershipCount` | integer |

**Foreign keys:**
- `productId` → `products.id`
- `cartId` → `carts.id`

### `cart_taxes` {#table-cart-taxes}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `taxName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | cart_taxes_type_enum |
| `taxCategory` | cart_taxes_taxcategory_enum |

**Foreign keys:**
- `cartId` → `carts.id`

### `carts` {#table-carts}

| Column | Type |
|--------|------|
| `id` | serial |
| `reference` | character varying |
| `cartState` | carts_cartstate_enum |
| `userBID` | character varying |
| `billingAddressId` | integer |
| `shippingAddressId` | integer |
| `paymentMethodId` | integer |
| `subTotal` | numeric |
| `feesTotal` | numeric |
| `taxTotal` | numeric |
| `grandTotal` | numeric |
| `cartAssetId` | integer |
| `isActive` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `commissionSubTotal` | numeric |
| `userSubscriptionType` | character varying |
| `utilityToken` | numeric |
| `smartPayPercentage` | numeric |
| `estimatedDelivery` | numeric |
| `isSmartPay` | boolean |

**Foreign keys:**
- `shippingAddressId` → `user_addresses.id`
- `paymentMethodId` → `payment_methods.id`
- `cartAssetId` → `cart_assets.id`
- `billingAddressId` → `user_addresses.id`

### `categories` {#table-categories}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | text |
| `code` | categories_code_enum |
| `displayOrder` | integer |
| `categoryId` | integer |
| `image` | text |
| `isActive` | boolean |
| `isDisplay` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

### `connect_queue_item` {#table-connect-queue-item}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `orderTransactionId` | integer |
| `status` | character varying |
| `latestRequestBody` | jsonb |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `orderTransactionId` → `order_transactions.id`

### `countries` {#table-countries}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | character varying |
| `code` | character varying |
| `alphaCode` | character varying |
| `callingCode` | character varying |
| `flag` | character varying |
| `minPhoneLength` | character varying |
| `zipCodeExists` | boolean |
| `zipCodeRegex` | character varying |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `zipCodeExample` | character varying |
| `isCheckoutEnabled` | boolean |

### `country_cities` {#table-country-cities}

| Column | Type |
|--------|------|
| `id` | serial |
| `countryId` | integer |
| `stateId` | integer |
| `name` | character varying |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `stateId` → `country_states.id`
- `countryId` → `countries.id`

### `country_states` {#table-country-states}

| Column | Type |
|--------|------|
| `id` | serial |
| `countryId` | integer |
| `name` | character varying |
| `code` | character varying |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `countryId` → `countries.id`

### `credit_notes` {#table-credit-notes}

| Column | Type |
|--------|------|
| `id` | serial |
| `identifier` | character varying |
| `createdFor` | character varying |
| `type` | character varying |
| `creditNoteInvoiceFileName` | character varying |
| `orderId` | integer |
| `shipmentOrderId` | integer |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `orderId` → `orders.id`
- `shipmentOrderId` → `shipment_orders.id`

### `devices` {#table-devices}

| Column | Type |
|--------|------|
| `id` | serial |
| `serialNumber` | character varying |
| `linkedItemIdentifier` | character varying |
| `imei` | jsonb |
| `mac` | character varying |
| `wan` | character varying |
| `lan` | character varying |
| `type` | character varying |
| `isLinked` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `linkedAt` | timestamp without time zone |
| `linkedLegacyItemIdentifier` | character varying |
| `isLegacyLinked` | boolean |

### `email_histories` {#table-email-histories}

| Column | Type |
|--------|------|
| `id` | serial |
| `userBID` | character varying |
| `fromEmail` | character varying |
| `toEmail` | character varying |
| `subject` | character varying |
| `orderId` | character varying |
| `status` | character varying |
| `type` | character varying |
| `responseData` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `shipmentOrderId` | character varying |

### `extension_cart_assets` {#table-extension-cart-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `assetOption` | jsonb |
| `calculatedCommision` | jsonb |
| `baseAssetName` | character varying |
| `baseAssetSymbol` | character varying |
| `baseAssetAmount` | numeric |
| `baseAssetPercentage` | numeric |
| `optionAssetName` | character varying |
| `optionAssetSymbol` | character varying |
| `optionAssetAmount` | numeric |
| `optionAssetPercentage` | numeric |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `cartId` → `extension_carts.id`

### `extension_cart_cashbacks` {#table-extension-cart-cashbacks}

| Column | Type |
|--------|------|
| `id` | serial |
| `extensionCartId` | integer |
| `assetName` | character varying |
| `assetSymbol` | character varying |
| `cashbackAssetId` | integer |
| `totalAmount` | numeric |

**Foreign keys:**
- `extensionCartId` → `extension_carts.id`
- `cashbackAssetId` → `shipping_cashback_assets.id`

### `extension_cart_fees` {#table-extension-cart-fees}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `feeName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | extension_cart_fees_type_enum |
| `feeCategory` | "extension_cart_fees_feeCategory_enum" |

**Foreign keys:**
- `cartId` → `extension_carts.id`

### `extension_cart_products` {#table-extension-cart-products}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `productId` | integer |
| `orderUnitExtensionId` | integer |
| `price` | numeric |
| `originalPrice` | numeric |
| `discount` | numeric |
| `isEligibleForDiscount` | boolean |
| `discountedPercentage` | numeric |
| `quantity` | integer |
| `isEligibleForCommission` | boolean |
| `commission` | jsonb |
| `canProductBeRemoved` | boolean |
| `feedBackMessage` | character varying |
| `userPurchaseLimit` | integer |
| `canUserPurchaseTheProduct` | boolean |
| `totalOrderExistsForProduct` | integer |
| `maximumUserCanPurchase` | integer |
| `shippingItems` | jsonb |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `orderUnitExtensionId` → `order_unit_extension_eligibilities.id`
- `productId` → `products.id`
- `cartId` → `extension_carts.id`

### `extension_cart_taxes` {#table-extension-cart-taxes}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `taxName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | extension_cart_taxes_type_enum |
| `taxCategory` | "extension_cart_taxes_taxCategory_enum" |

**Foreign keys:**
- `cartId` → `extension_carts.id`

### `extension_carts` {#table-extension-carts}

| Column | Type |
|--------|------|
| `id` | serial |
| `reference` | character varying |
| `cartState` | extension_carts_cartstate_enum |
| `userBID` | character varying |
| `billingAddressId` | integer |
| `shippingAddressId` | integer |
| `paymentMethodId` | integer |
| `shippingMethodId` | integer |
| `storeId` | integer |
| `commissionSubTotal` | numeric |
| `subTotal` | numeric |
| `feesTotal` | numeric |
| `discountTotal` | numeric |
| `vouchers` | jsonb |
| `shippingTotal` | numeric |
| `taxTotal` | numeric |
| `grandTotal` | numeric |
| `userSubscriptionType` | character varying |
| `isActive` | boolean |
| `isSmartPay` | boolean |
| `isShippingApplicable` | boolean |
| `orderId` | character varying |
| `orderUniqueId` | integer |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `paymentMethodId` → `payment_methods.id`
- `billingAddressId` → `user_addresses.id`
- `storeId` → `stores.id`
- `shippingMethodId` → `shipping_methods.id`
- `shippingAddressId` → `user_addresses.id`

### `feature_flags` {#table-feature-flags}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | character varying |
| `code` | character varying |
| `autoDeployAt` | timestamp without time zone |
| `autoDeploy` | boolean |
| `isActive` | boolean |

### `gen2_gen3_orders_migration_map` {#table-gen2-gen3-orders-migration-map}

| Column | Type |
|--------|------|
| `id` | serial |
| `gen2OrderId` | integer |
| `gen3OrderId` | character varying |
| `userBID` | character varying |
| `createdAt` | timestamp without time zone |

**Foreign keys:**
- `gen2OrderId` → `orders.id`
- `gen3OrderId` → `orders.orderId`

### `gen2_migration_eligibility_v2` {#table-gen2-migration-eligibility-v2}

| Column | Type |
|--------|------|
| `id` | uuid |
| `userBID` | character varying |
| `gen2OrderId` | integer |
| `gen2ShipmentItemId` | integer |
| `migrationStatus` | character varying |
| `eligibleGen3ProductId` | integer |
| `eligibleQuantity` | integer |
| `eligibleDiscountPercentage` | numeric(5, 2) |
| `eligiblePrice` | numeric(12, 2) |
| `migrationCategory` | character varying |
| `cashbackAsset` | character varying |
| `refundApplicable` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `gen2ShipmentStatusAtCreation` | character varying |
| `eligibleShippingCost` | numeric(12, 2) |

### `gen2_migration_queue_items` {#table-gen2-migration-queue-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `gen2OrderId` | character varying |
| `userBID` | character varying |
| `migrationEligibilityId` | character varying |
| `gen2ShipmentIdentifier` | character varying |
| `gen2Sku` | character varying |
| `gen2ProductName` | character varying |
| `gen3OrderId` | character varying |
| `gen3ShipmentItems` | jsonb |
| `latestRequestBody` | jsonb |
| `status` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

### `gen2_shipment_migration_config` {#table-gen2-shipment-migration-config}

| Column | Type |
|--------|------|
| `id` | uuid |
| `migrationCategory` | character varying |
| `sku` | character varying |
| `mappedSku` | character varying |
| `quantity` | integer |
| `refundAmountUSD` | numeric |
| `refundApplicable` | boolean |
| `cashbackAsset` | character varying |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `shippingCost` | numeric(12, 2) |
| `productPrice` | numeric(12, 2) |
| `discountPercentage` | numeric |

### `ioss_queue_item` {#table-ioss-queue-item}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `orderTransactionId` | integer |
| `status` | character varying |
| `latestRequestBody` | jsonb |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `orderTransactionId` → `order_transactions.id`

### `legacy_order_items` {#table-legacy-order-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | integer |
| `productId` | character varying |
| `name` | character varying |
| `sku` | character varying |
| `reference` | character varying |
| `categoryId` | character varying |
| `categoryName` | character varying |
| `categoryCode` | character varying |
| `details` | text |
| `summary` | text |
| `metadata` | jsonb |
| `kitData` | jsonb |
| `price` | numeric |
| `quantity` | integer |
| `featureImage` | text |
| `weight` | numeric |
| `isActive` | boolean |
| `isEligibleForCommission` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `isUpgradable` | boolean |
| `legacySku` | character varying |

**Foreign keys:**
- `orderId` → `legacy_orders.id`

### `legacy_orders` {#table-legacy-orders}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `invoiceId` | integer |
| `reference` | character varying |
| `userBID` | character varying |
| `status` | character varying |
| `billingAddress` | jsonb |
| `paymentBillingAddress` | jsonb |
| `shippingAddress` | jsonb |
| `paymentMethodId` | integer |
| `paymentMethod` | jsonb |
| `paymentStatus` | character varying |
| `commissionSubTotal` | numeric |
| `subTotal` | numeric |
| `fees` | jsonb |
| `feesTotal` | numeric |
| `assetOption` | jsonb |
| `discountTotal` | numeric |
| `taxes` | jsonb |
| `taxTotal` | numeric |
| `grandTotal` | numeric |
| `isConsentAccepted` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `version` | integer |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `invoiceSequenceNumber` | integer |
| `exchangeRate` | numeric |
| `paymentAssetName` | character varying |

**Foreign keys:**
- `invoiceId` → `order_invoices.id`

### `legacy_shipment_items` {#table-legacy-shipment-items}

| Column | Type |
|--------|------|
| `id` | uuid |
| `userBID` | character varying |
| `legacyOrderIdentifier` | character varying |
| `legacyOrderId` | integer |
| `legacyOrderItemId` | integer |
| `assignedSerialNumber` | character varying |
| `itemIdentifier` | character varying |
| `sku` | character varying |
| `legacySku` | character varying |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `isActive` | boolean |
| `status` | character varying |

### `legacy_shipment_status_update_queue_items` {#table-legacy-shipment-status-update-queue-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `jobId` | character varying |
| `shipmentStatus` | character varying |
| `shipmentItemIdentifier` | character varying |
| `assignedSerialNumber` | character varying |
| `remark` | character varying |
| `shipmentTrackingId` | character varying |
| `shipmentTrackingUrl` | character varying |
| `userBID` | character varying |
| `productId` | character varying |
| `latestRequestBody` | jsonb |
| `status` | character varying |
| `eventLogs` | jsonb |
| `timestamp` | timestamp without time zone |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `isSnChanged` | boolean |
| `isSnRemoved` | boolean |

### `machine_extension_queue_items` {#table-machine-extension-queue-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `machineOrderId` | character varying |
| `extensionOrderId` | character varying |
| `userBID` | character varying |
| `orderUnitExtensionId` | character varying |
| `machineOrderUnitIdentifier` | character varying |
| `sku` | character varying |
| `productName` | character varying |
| `extensions` | jsonb |
| `gen3OrderId` | character varying |
| `latestRequestBody` | jsonb |
| `status` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `purchasedAt` | timestamp with time zone |
| `deliveryStatus` | character varying(100) |

### `machine_upgrade_queue_item` {#table-machine-upgrade-queue-item}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `legacyMachineOrderIdentifier` | character varying |
| `upgradableItemId` | uuid |
| `latestRequestBody` | jsonb |
| `status` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `upgradableItemId` → `upgradable_items.id`

### `migration_cart_assets` {#table-migration-cart-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `assetOption` | jsonb |
| `calculatedCommision` | jsonb |
| `baseAssetName` | character varying |
| `baseAssetSymbol` | character varying |
| `baseAssetAmount` | numeric |
| `baseAssetPercentage` | numeric |
| `optionAssetName` | character varying |
| `optionAssetSymbol` | character varying |
| `optionAssetAmount` | numeric |
| `optionAssetPercentage` | numeric |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `cartId` → `migration_carts.id`

### `migration_cart_cashbacks` {#table-migration-cart-cashbacks}

| Column | Type |
|--------|------|
| `id` | serial |
| `migrationCartId` | integer |
| `assetName` | character varying |
| `assetSymbol` | character varying |
| `cashbackAssetId` | integer |
| `totalAmount` | numeric |

**Foreign keys:**
- `cashbackAssetId` → `shipping_cashback_assets.id`
- `migrationCartId` → `migration_carts.id`

### `migration_cart_fees` {#table-migration-cart-fees}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `feeName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | migration_cart_fees_type_enum |
| `feeCategory` | migration_cart_fees_feecategory_enum |

**Foreign keys:**
- `cartId` → `migration_carts.id`

### `migration_cart_products` {#table-migration-cart-products}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `productId` | integer |
| `shipmentItemId` | integer |
| `gen2MigrationEligibilityId` | uuid |
| `price` | numeric |
| `originalPrice` | numeric |
| `discount` | numeric |
| `isEligibleForDiscount` | boolean |
| `discountedPercentage` | numeric |
| `quantity` | integer |
| `isEligibleForCommission` | boolean |
| `commission` | jsonb |
| `canProductBeRemoved` | boolean |
| `feedBackMessage` | character varying |
| `userPurchaseLimit` | integer |
| `canUserPurchaseTheProduct` | boolean |
| `totalOrderExistsForProduct` | integer |
| `maximumUserCanPurchase` | integer |
| `shippingItems` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `productId` → `products.id`
- `cartId` → `migration_carts.id`
- `shipmentItemId` → `shipment_items.id`
- `gen2MigrationEligibilityId` → `gen2_migration_eligibility_v2.id`

### `migration_cart_taxes` {#table-migration-cart-taxes}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `taxName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | migration_cart_taxes_type_enum |
| `taxCategory` | migration_cart_taxes_taxcategory_enum |

**Foreign keys:**
- `cartId` → `migration_carts.id`

### `migration_carts` {#table-migration-carts}

| Column | Type |
|--------|------|
| `id` | serial |
| `reference` | character varying |
| `cartState` | migration_carts_cartstate_enum |
| `userBID` | character varying |
| `billingAddressId` | integer |
| `shippingAddressId` | integer |
| `paymentMethodId` | integer |
| `shippingMethodId` | integer |
| `storeId` | integer |
| `commissionSubTotal` | numeric |
| `subTotal` | numeric |
| `feesTotal` | numeric |
| `discountTotal` | numeric |
| `vouchers` | jsonb |
| `shippingTotal` | numeric |
| `taxTotal` | numeric |
| `grandTotal` | numeric |
| `cartAssetId` | integer |
| `userSubscriptionType` | character varying |
| `isActive` | boolean |
| `isSmartPay` | boolean |
| `isShippingApplicable` | boolean |
| `gen2OrderId` | character varying |
| `gen2OrderUniqueId` | integer |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `cartAssetId` → `migration_cart_assets.id`
- `storeId` → `stores.id`
- `shippingMethodId` → `shipping_methods.id`
- `paymentMethodId` → `payment_methods.id`
- `billingAddressId` → `user_addresses.id`
- `shippingAddressId` → `user_addresses.id`

### `migration_refund_request_items` {#table-migration-refund-request-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `migrationRefundRequestId` | integer |
| `shipmentCashbackQueueItemId` | integer |
| `refundAssetSymbol` | character varying |
| `refundAmount` | numeric |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `shipmentCashbackQueueItemId` → `shipping_cashback_queue_item.id`
- `migrationRefundRequestId` → `migration_refund_requests.id`

### `migration_refund_requests` {#table-migration-refund-requests}

| Column | Type |
|--------|------|
| `id` | serial |
| `gen2Gen3OrdersMigrationMapId` | integer |
| `refundStatus` | migration_refund_requests_refundstatus_enum |
| `shipmentOrderToBeRefunded` | character varying |
| `refundBaseAssetSymbol` | character varying |
| `refundBaseAssetAmountPercentage` | numeric |
| `refundOptionAssetSymbol` | character varying |
| `refundOptionAssetAmountPercentage` | numeric |
| `totalAmountToRefund` | numeric |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `userBID` | character varying |
| `shipmentOrderId` | integer |

**Foreign keys:**
- `shipmentOrderId` → `shipment_orders.id`
- `gen2Gen3OrdersMigrationMapId` → `gen2_gen3_orders_migration_map.id`

### `migrations` {#table-migrations}

| Column | Type |
|--------|------|
| `id` | serial |
| `timestamp` | bigint |
| `name` | character varying |

### `order_invoices` {#table-order-invoices}

| Column | Type |
|--------|------|
| `id` | serial |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `orderId` | integer |
| `invoiceSequenceNumber` | integer |
| `invoiceFileName` | character varying |

**Foreign keys:**
- `orderId` → `orders.id`

### `order_item_units` {#table-order-item-units}

| Column | Type |
|--------|------|
| `id` | bigserial |
| `orderId` | character varying(100) |
| `orderItemId` | integer |
| `productSku` | character varying(100) |
| `mainProductSku` | character varying(100) |
| `isShipmentNeeded` | boolean |
| `categoryCode` | character varying(100) |
| `userBID` | character varying(100) |
| `uniqueItemIdentifier` | character varying(150) |
| `attributes` | jsonb |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `purchasedAt` | timestamp with time zone |

**Foreign keys:**
- `orderItemId` → `order_items.id`

### `order_items` {#table-order-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | integer |
| `productId` | integer |
| `name` | character varying |
| `sku` | character varying |
| `reference` | character varying |
| `categoryId` | integer |
| `categoryName` | character varying |
| `categoryCode` | character varying |
| `details` | text |
| `summary` | text |
| `metadata` | jsonb |
| `kitData` | jsonb |
| `price` | numeric |
| `quantity` | integer |
| `featureImage` | text |
| `weight` | numeric |
| `isActive` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `isEligibleForCommission` | boolean |
| `upgradableItemIds` | text |
| `discount` | numeric |
| `enforcedShippingItems` | jsonb |
| `status` | character varying |
| `statusChangeLogs` | jsonb |
| `smartPayOriginalPrice` | numeric |
| `utilityToken` | numeric |
| `smartPayPercentage` | numeric |
| `gen2MigrationEligibilityId` | uuid |

**Foreign keys:**
- `orderId` → `orders.id`
- `gen2MigrationEligibilityId` → `gen2_migration_eligibility_v2.id`

### `order_items_v1` {#table-order-items-v1}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | integer |
| `productId` | integer |
| `name` | character varying |
| `sku` | character varying |
| `reference` | character varying |
| `categoryId` | integer |
| `categoryName` | character varying |
| `categoryCode` | character varying |
| `details` | text |
| `summary` | text |
| `metadata` | jsonb |
| `kitData` | jsonb |
| `price` | numeric |
| `quantity` | integer |
| `featureImage` | text |
| `weight` | numeric |
| `isActive` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `isEligibleForCommission` | boolean |

**Foreign keys:**
- `orderId` → `orders_v1.id`

### `order_shipping_address_histories` {#table-order-shipping-address-histories}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderInternalId` | integer |
| `shipmentOrderInternalId` | integer |
| `oldShippingAddress` | jsonb |
| `newShippingAddress` | jsonb |
| `partnerHubRequest` | jsonb |
| `partnerHubResponse` | jsonb |
| `changedByAdminId` | integer |
| `changedByAdminEmail` | character varying |
| `removedOrderInvoiceFileName` | character varying |
| `removedShipmentInvoiceFileName` | character varying |
| `status` | character varying |
| `createdAt` | timestamp without time zone |

**Foreign keys:**
- `orderInternalId` → `orders.id`

### `order_transaction_v1` {#table-order-transaction-v1}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | integer |
| `paymentMethodId` | integer |
| `paymentStatus` | character varying |
| `paymentMethodProvider` | character varying |
| `paymentMethodCode` | character varying |
| `response` | jsonb |
| `exchangeRate` | numeric |
| `errorMessage` | character varying |
| `trackingId` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `orderId` → `orders_v1.id`

### `order_transactions` {#table-order-transactions}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | integer |
| `paymentMethodId` | integer |
| `paymentStatus` | character varying |
| `paymentMethodProvider` | character varying |
| `paymentMethodCode` | character varying |
| `response` | jsonb |
| `exchangeRate` | numeric |
| `errorMessage` | character varying |
| `trackingId` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `orderId` → `orders.id`

### `order_unit_extension_eligibilities` {#table-order-unit-extension-eligibilities}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderUnitId` | integer |
| `orderId` | character varying(100) |
| `productSku` | character varying(100) |
| `extensionProductSku` | character varying(100) |
| `maxQuantity` | integer |
| `extensionUnitPrice` | numeric |
| `shippingCostPerUnit` | numeric |
| `status` | character varying |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `userBID` | character varying(100) |
| `extensionOrderId` | character varying(100) |
| `cashbackAsset` | character varying |
| `eligibleDiscountPercentage` | numeric(5, 2) |

**Foreign keys:**
- `extensionProductSku` → `products.sku`

### `orders` {#table-orders}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `invoiceId` | integer |
| `reference` | character varying |
| `userBID` | character varying |
| `status` | character varying |
| `billingAddress` | jsonb |
| `paymentBillingAddress` | jsonb |
| `shippingAddress` | jsonb |
| `paymentMethodId` | integer |
| `paymentMethod` | jsonb |
| `paymentStatus` | character varying |
| `subTotal` | numeric |
| `fees` | jsonb |
| `feesTotal` | numeric |
| `assetOption` | jsonb |
| `discountTotal` | numeric |
| `taxes` | jsonb |
| `taxTotal` | numeric |
| `grandTotal` | numeric |
| `isConsentAccepted` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `version` | integer |
| `importedData` | boolean |
| `importDate` | timestamp without time zone |
| `importSource` | character varying |
| `commissionSubTotal` | numeric |
| `userSubscriptionType` | character varying |
| `createdByAdmin` | boolean |
| `adminEmail` | character varying |
| `adminRemark` | character varying |
| `vouchers` | jsonb |
| `shippingTotal` | numeric |
| `isUpgrade` | boolean |
| `upgradableItemIds` | text |
| `enforcedShipping` | boolean |
| `shippingMethod` | jsonb |
| `store` | jsonb |
| `legacyOrderId` | character varying |
| `legacyOrderUniqueId` | integer |
| `cashBacks` | jsonb |
| `statusChangeLogs` | jsonb |
| `productBoost` | numeric |
| `utilityToken` | numeric |
| `isSmartPay` | boolean |
| `smartPayPercentage` | numeric |
| `smartPayTotals` | jsonb |
| `isGen2Migration` | boolean |
| `email` | character varying |
| `isExtension` | boolean |
| `partnerHubShippingAddressVerifiedAt` | timestamp without time zone |

**Foreign keys:**
- `invoiceId` → `order_invoices.id`

### `orders_v1` {#table-orders-v1}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `invoiceId` | integer |
| `reference` | character varying |
| `userBID` | character varying |
| `status` | character varying |
| `billingAddress` | jsonb |
| `paymentBillingAddress` | jsonb |
| `shippingAddress` | jsonb |
| `paymentMethodId` | integer |
| `paymentMethod` | jsonb |
| `paymentStatus` | character varying |
| `subTotal` | numeric |
| `fees` | jsonb |
| `feesTotal` | numeric |
| `assetOption` | jsonb |
| `discountTotal` | numeric |
| `taxes` | jsonb |
| `taxTotal` | numeric |
| `grandTotal` | numeric |
| `isConsentAccepted` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `version` | integer |
| `importedData` | boolean |
| `importDate` | timestamp without time zone |
| `importSource` | character varying |
| `commissionSubTotal` | numeric |
| `userSubscriptionType` | character varying |
| `createdByAdmin` | boolean |
| `adminEmail` | character varying |
| `adminRemark` | character varying |

**Foreign keys:**
- `invoiceId` → `order_invoices.id`

### `partner_hub_bulk_address_verify_job_items` {#table-partner-hub-bulk-address-verify-job-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `jobId` | integer |
| `orderId` | character varying |
| `status` | partner_hub_bulk_address_verify_item_status_enum |
| `message` | text |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `processedAt` | timestamp with time zone |

**Foreign keys:**
- `jobId` → `partner_hub_bulk_address_verify_jobs.id`

### `partner_hub_bulk_address_verify_jobs` {#table-partner-hub-bulk-address-verify-jobs}

| Column | Type |
|--------|------|
| `id` | serial |
| `status` | partner_hub_bulk_address_verify_job_status_enum |
| `totalCount` | integer |
| `processedCount` | integer |
| `successCount` | integer |
| `skippedCount` | integer |
| `failedCount` | integer |
| `createdByAdminId` | integer |
| `createdByAdminEmail` | character varying |
| `errorMessage` | text |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `completedAt` | timestamp with time zone |

### `partner_hub_order_address_sync_logs` {#table-partner-hub-order-address-sync-logs}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying(64) |
| `attemptNumber` | integer |
| `requestBody` | jsonb |
| `responseBody` | jsonb |
| `status` | partner_hub_order_address_sync_logs_status_enum |
| `httpStatusCode` | integer |
| `createdAt` | timestamp with time zone |

### `payment_assets` {#table-payment-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `paymentMethodId` | integer |
| `name` | character varying |
| `symbol` | character varying |
| `displayOrder` | integer |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `paymentMethodId` → `payment_methods.id`

### `payment_callbacks` {#table-payment-callbacks}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `transactionId` | character varying |
| `paymentStatus` | character varying |
| `paymentMethodCode` | character varying |
| `paymentMethodProvider` | character varying |
| `callbackPayload` | jsonb |
| `errorMessage` | character varying |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

### `payment_fees` {#table-payment-fees}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | character varying |
| `value` | numeric |
| `type` | payment_fees_type_enum |
| `feeCategory` | payment_fees_feecategory_enum |
| `paymentMethodId` | integer |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `paymentMethodId` → `payment_methods.id`

### `payment_methods` {#table-payment-methods}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | character varying |
| `code` | payment_methods_code_enum |
| `provider` | payment_methods_provider_enum |
| `displayOrder` | integer |
| `isVariable` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `isConsentRequired` | boolean |
| `isShippingEnable` | boolean |
| `isUpgradeEnable` | boolean |
| `isSmartPayEnable` | boolean |
| `isGen2MigrationEnable` | boolean |

### `payment_options` {#table-payment-options}

| Column | Type |
|--------|------|
| `id` | serial |
| `fromAssetId` | integer |
| `optionId` | integer |
| `minPercentage` | integer |
| `isVariable` | boolean |
| `commissionMultiplier` | jsonb |
| `isCommissionEnabled` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `isShippingEnable` | boolean |
| `displayStatus` | boolean |
| `isUpgradeEnable` | boolean |
| `isSmartPayEnable` | boolean |
| `isGen2MigrationEnable` | boolean |
| `isShippingRepaymentEnable` | boolean |

**Foreign keys:**
- `optionId` → `payment_assets.id`
- `fromAssetId` → `payment_assets.id`

### `payment_restrictions` {#table-payment-restrictions}

| Column | Type |
|--------|------|
| `id` | serial |
| `productId` | integer |
| `categoryId` | integer |
| `paymentOptionId` | integer |
| `isNotAllowed` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `categoryId` → `categories.id`
- `paymentOptionId` → `payment_options.id`
- `productId` → `products.id`

### `product_eligibility_criterias` {#table-product-eligibility-criterias}

| Column | Type |
|--------|------|
| `id` | serial |
| `currentUserSubscriptionType` | product_eligibility_criterias_currentusersubscriptiontype_enum |
| `hasActiveFirstLine` | boolean |
| `isSubscriptionActive` | boolean |
| `eligibileProductSKU` | character varying |
| `categoryCode` | character varying |
| `isProductPurchasable` | boolean |
| `isActive` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

### `product_extension_configurations` {#table-product-extension-configurations}

| Column | Type |
|--------|------|
| `id` | serial |
| `mainProductSku` | character varying(100) |
| `extensionProductSku` | character varying(100) |
| `maxQuantity` | integer |
| `extensionUnitPrice` | numeric(10, 2) |
| `shippingCostPerUnit` | numeric(10, 2) |
| `isActive` | boolean |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |
| `cashbackAsset` | character varying |
| `discountPercentage` | numeric(5, 2) |

### `product_files` {#table-product-files}

| Column | Type |
|--------|------|
| `id` | serial |
| `url` | text |
| `type` | character varying |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

### `product_images` {#table-product-images}

| Column | Type |
|--------|------|
| `productId` | integer |
| `productFileId` | integer |

**Foreign keys:**
- `productFileId` → `product_files.id`
- `productId` → `products.id`

### `product_shipment_configurations` {#table-product-shipment-configurations}

| Column | Type |
|--------|------|
| `id` | serial |
| `productId` | integer |
| `upgradeCost` | numeric |
| `pickupCost` | numeric |
| `usePickupStoreFee` | boolean |
| `shippingMethodId` | integer |
| `isShipmentEnabled` | boolean |

**Foreign keys:**
- `shippingMethodId` → `shipping_methods.id`
- `productId` → `products.id`

### `product_shipping_cashback_assets` {#table-product-shipping-cashback-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `productId` | integer |
| `cashbackAssetId` | integer |
| `shippingMethodId` | integer |
| `value` | numeric |
| `type` | product_shipping_cashback_assets_type_enum |
| `isActive` | boolean |
| `isDisplay` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `cashbackAssetId` → `shipping_cashback_assets.id`
- `shippingMethodId` → `shipping_methods.id`

### `product_shipping_costs` {#table-product-shipping-costs}

| Column | Type |
|--------|------|
| `id` | serial |
| `productId` | integer |
| `shippingProviderId` | integer |
| `countryId` | integer |
| `shippingMethodId` | integer |
| `cost` | numeric |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `countryId` → `countries.id`
- `productId` → `products.id`
- `shippingProviderId` → `shipping_providers.id`
- `shippingMethodId` → `shipping_methods.id`

### `product_tags` {#table-product-tags}

| Column | Type |
|--------|------|
| `productId` | integer |
| `tagId` | integer |

**Foreign keys:**
- `productId` → `products.id`
- `tagId` → `tags.id`

### `product_upgrades` {#table-product-upgrades}

| Column | Type |
|--------|------|
| `id` | serial |
| `upgradableProductId` | integer |
| `upgradeProductId` | integer |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `cost` | numeric |
| `upgradableProductSkuId` | character varying |
| `quantity` | numeric |
| `enforceShipping` | boolean |
| `upgradeOnly` | boolean |
| `isEligibleForCommission` | boolean |
| `voucherName` | character varying |

**Foreign keys:**
- `upgradableProductId` → `products.id`
- `upgradeProductId` → `products.id`

### `products` {#table-products}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | character varying |
| `sku` | character varying |
| `categoryId` | integer |
| `displayOrder` | integer |
| `details` | text |
| `summary` | text |
| `overview` | text |
| `metadata` | jsonb |
| `specification` | text |
| `features` | text |
| `price` | numeric |
| `userPurchaseLimit` | integer |
| `quantity` | integer |
| `featureImage` | text |
| `weight` | numeric |
| `isActive` | boolean |
| `isDisplay` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `isEligibleForCommission` | boolean |
| `maxCartQuantity` | integer |
| `isShipmentNeeded` | boolean |
| `oneCarePrice` | numeric |
| `isUpgradable` | boolean |
| `reference` | uuid |
| `utilityToken` | numeric |
| `smartPayPercentage` | numeric |
| `smartPayAmount` | numeric |
| `estimatedDeliveryCost` | numeric |

**Foreign keys:**
- `categoryId` → `categories.id`

### `queue_partner_hub_orders` {#table-queue-partner-hub-orders}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `orderTransactionId` | integer |
| `status` | character varying |
| `eventLogs` | jsonb |
| `latestRequestBody` | jsonb |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

### `send_gen_histories` {#table-send-gen-histories}

| Column | Type |
|--------|------|
| `id` | serial |
| `requestId` | character varying |
| `itemId` | character varying |
| `payLoad` | jsonb |
| `callBackReceived` | boolean |
| `type` | character varying |
| `responseData` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

### `shipment_item_logs` {#table-shipment-item-logs}

| Column | Type |
|--------|------|
| `id` | serial |
| `statusChangedFrom` | shipment_item_logs_statuschangedfrom_enum |
| `statusChangedTo` | shipment_item_logs_statuschangedto_enum |
| `updatedBy` | shipment_item_logs_updatedby_enum |
| `adminEmail` | character varying |
| `note` | character varying |
| `shipmentItemId` | integer |
| `createdAt` | timestamp without time zone |
| `shipmentTrackingId` | character varying |
| `waybillNumber` | character varying(255) |

**Foreign keys:**
- `shipmentItemId` → `shipment_items.id`

### `shipment_items` {#table-shipment-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderItemId` | integer |
| `orderId` | integer |
| `productId` | integer |
| `userBID` | character varying |
| `shipmentStatus` | shipment_items_shipmentstatus_enum |
| `shipmentItemIdentifier` | character varying |
| `shippingMethodId` | integer |
| `pickupStoreId` | integer |
| `oneCarePurchased` | boolean |
| `shippingAddressDetails` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `statusUpdatedAt` | timestamp without time zone |
| `assignedSerialNumber` | character varying |
| `shipmentTrackingId` | character varying |
| `shipmentItemType` | character varying |
| `waybillNumber` | character varying(255) |
| `deliveryEmailSentAt` | timestamp with time zone |

**Foreign keys:**
- `orderItemId` → `order_items.id`
- `productId` → `products.id`
- `shippingMethodId` → `shipping_methods.id`
- `orderId` → `orders.id`
- `pickupStoreId` → `stores.id`

### `shipment_order_invoices` {#table-shipment-order-invoices}

| Column | Type |
|--------|------|
| `id` | serial |
| `shipmentOrderId` | integer |
| `invoiceSequenceNumber` | integer |
| `invoiceFileName` | character varying |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `shipmentOrderId` → `shipment_orders.id`

### `shipment_order_items` {#table-shipment-order-items}

| Column | Type |
|--------|------|
| `id` | serial |
| `shipmentOrderId` | integer |
| `shippingCost` | numeric |
| `oneCarePrice` | numeric |
| `upgradeCost` | numeric |
| `oneCareIncluded` | boolean |
| `pickupCost` | numeric |
| `totalCostOfShipment` | numeric |
| `quantity` | integer |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `shipmentItemId` | integer |
| `statusChangeLogs` | jsonb |
| `isReturned` | boolean |

**Foreign keys:**
- `shipmentItemId` → `shipment_items.id`
- `shipmentOrderId` → `shipment_orders.id`

### `shipment_order_transactions` {#table-shipment-order-transactions}

| Column | Type |
|--------|------|
| `id` | serial |
| `shipmentOrderId` | integer |
| `paymentMethodId` | integer |
| `paymentStatus` | character varying |
| `paymentMethodProvider` | character varying |
| `paymentMethodCode` | character varying |
| `response` | jsonb |
| `exchangeRate` | numeric |
| `errorMessage` | character varying |
| `trackingId` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `shipmentOrderId` → `shipment_orders.id`

### `shipment_orders` {#table-shipment-orders}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `orderUniqueId` | integer |
| `shippingMethodId` | integer |
| `storeId` | integer |
| `shipmentOrderId` | character varying |
| `shipmentInvoiceId` | integer |
| `reference` | character varying |
| `userBID` | character varying |
| `userSubscriptionType` | character varying |
| `status` | character varying |
| `billingAddress` | jsonb |
| `paymentBillingAddress` | jsonb |
| `shippingAddress` | jsonb |
| `paymentMethodId` | integer |
| `paymentMethod` | jsonb |
| `paymentStatus` | character varying |
| `oneCareTotal` | numeric |
| `subTotal` | numeric |
| `fees` | jsonb |
| `feesTotal` | numeric |
| `taxes` | jsonb |
| `taxTotal` | numeric |
| `assetOption` | jsonb |
| `grandTotal` | numeric |
| `cashBacks` | jsonb |
| `isConsentAccepted` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `version` | integer |
| `enforcedShipping` | boolean |
| `statusChangeLogs` | jsonb |
| `isSmartPay` | boolean |
| `email` | character varying |
| `isGen2Migration` | boolean |
| `isExtension` | boolean |
| `shipmentOrderType` | shipping_cart_type_enum |

**Foreign keys:**
- `orderUniqueId` → `orders.id`
- `shippingMethodId` → `shipping_methods.id`
- `shipmentInvoiceId` → `shipment_order_invoices.id`
- `storeId` → `stores.id`

### `shipment_status_update_queue_item` {#table-shipment-status-update-queue-item}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `jobId` | character varying |
| `shipmentStatus` | shipment_status_update_queue_item_shipmentstatus_enum |
| `shipmentItemIdentifier` | character varying |
| `assignedSerialNumber` | character varying |
| `remark` | character varying |
| `shipmentTrackingId` | character varying |
| `shipmentTrackingUrl` | character varying |
| `userBID` | character varying |
| `productId` | character varying |
| `latestRequestBody` | jsonb |
| `status` | character varying |
| `eventLogs` | jsonb |
| `timestamp` | timestamp without time zone |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `shipmentItemType` | character varying |

### `shipment_webhook_logs` {#table-shipment-webhook-logs}

| Column | Type |
|--------|------|
| `id` | serial |
| `webhookPath` | character varying |
| `orderId` | character varying |
| `requestId` | character varying |
| `userBID` | character varying |
| `shipmentTrackingId` | character varying |
| `preAssignedSerialNumber` | character varying |
| `shipmentItemIdentifier` | character varying |
| `itemSku` | character varying |
| `activityMessage` | character varying |
| `additionalInfo` | jsonb |
| `isSuccess` | boolean |
| `errorInfo` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `waybillNumber` | character varying(255) |

### `shipping_cart_assets` {#table-shipping-cart-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `shippingCartId` | integer |
| `assetOption` | jsonb |
| `calculatedCommission` | jsonb |
| `baseAssetName` | character varying |
| `baseAssetSymbol` | character varying |
| `baseAssetAmount` | numeric |
| `baseAssetPercentage` | numeric |
| `optionAssetName` | character varying |
| `optionAssetSymbol` | character varying |
| `optionAssetAmount` | numeric |
| `optionAssetPercentage` | numeric |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `shippingCartId` → `shipping_carts.id`

### `shipping_cart_cashbacks` {#table-shipping-cart-cashbacks}

| Column | Type |
|--------|------|
| `id` | serial |
| `shippingCartId` | integer |
| `assetName` | character varying |
| `assetSymbol` | character varying |
| `cashbackAssetId` | integer |
| `totalAmount` | numeric |

**Foreign keys:**
- `shippingCartId` → `shipping_carts.id`
- `cashbackAssetId` → `shipping_cashback_assets.id`

### `shipping_cart_fees` {#table-shipping-cart-fees}

| Column | Type |
|--------|------|
| `id` | serial |
| `shippingCartId` | integer |
| `feeName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | shipping_cart_fees_type_enum |
| `feeCategory` | shipping_cart_fees_feecategory_enum |

**Foreign keys:**
- `shippingCartId` → `shipping_carts.id`

### `shipping_cart_products` {#table-shipping-cart-products}

| Column | Type |
|--------|------|
| `id` | serial |
| `shippingCartId` | integer |
| `shipmentItemId` | integer |
| `shippingCost` | numeric |
| `oneCarePrice` | numeric |
| `upgradeCost` | numeric |
| `oneCareIncluded` | boolean |
| `pickupCost` | numeric |
| `totalCostOfShipment` | numeric |
| `quantity` | integer |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `notAllowedShippingMethods` | jsonb |

**Foreign keys:**
- `shippingCartId` → `shipping_carts.id`
- `shipmentItemId` → `shipment_items.id`

### `shipping_cart_taxes` {#table-shipping-cart-taxes}

| Column | Type |
|--------|------|
| `id` | serial |
| `shippingCartId` | integer |
| `taxName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | shipping_cart_taxes_type_enum |
| `taxCategory` | shipping_cart_taxes_taxcategory_enum |

**Foreign keys:**
- `shippingCartId` → `shipping_carts.id`

### `shipping_carts` {#table-shipping-carts}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartState` | shipping_carts_cartstate_enum |
| `userBID` | character varying |
| `orderId` | character varying |
| `shippingMethodId` | integer |
| `storeId` | integer |
| `billingAddressId` | integer |
| `shippingAddressId` | integer |
| `paymentMethodId` | integer |
| `subTotal` | numeric |
| `feesTotal` | numeric |
| `taxTotal` | numeric |
| `oneCareTotal` | numeric |
| `grandTotal` | numeric |
| `shippingCartAssetId` | integer |
| `isActive` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `isSmartPay` | boolean |
| `cartType` | shipping_cart_type_enum |

**Foreign keys:**
- `shippingMethodId` → `shipping_methods.id`
- `billingAddressId` → `user_addresses.id`
- `shippingCartAssetId` → `shipping_cart_assets.id`
- `paymentMethodId` → `payment_methods.id`
- `storeId` → `stores.id`
- `shippingAddressId` → `user_addresses.id`

### `shipping_cashback_assets` {#table-shipping-cashback-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `shippingMethodId` | integer |
| `assetName` | character varying |
| `assetSymbol` | character varying |
| `isDisplay` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

### `shipping_cashback_queue_item` {#table-shipping-cashback-queue-item}

| Column | Type |
|--------|------|
| `id` | serial |
| `shipmentOrderId` | character varying |
| `shipmentOrderTransactionId` | integer |
| `cashbackAmount` | numeric |
| `cashbackAssetSymbol` | character varying |
| `status` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `ShipmentOrderTransactionId` | integer |
| `userBID` | character varying |
| `latestRequestBody` | jsonb |

**Foreign keys:**
- `ShipmentOrderTransactionId` → `shipment_order_transactions.id`

### `shipping_methods` {#table-shipping-methods}

| Column | Type |
|--------|------|
| `id` | serial |
| `displayName` | character varying |
| `code` | shipping_methods_code_enum |
| `description` | character varying |
| `isActive` | boolean |
| `isDisplay` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

### `shipping_providers` {#table-shipping-providers}

| Column | Type |
|--------|------|
| `id` | serial |
| `displayName` | character varying |
| `shippingMethodId` | integer |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `deletedAt` | timestamp without time zone |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `shippingMethodId` → `shipping_methods.id`

### `shipping_repayment_config` {#table-shipping-repayment-config}

| Column | Type |
|--------|------|
| `id` | serial |
| `productId` | integer |
| `feeStrategy` | shipping_repayment_config_feestrategy_enum |
| `fixedAmount` | numeric(12, 2) |
| `isActive` | boolean |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `productId` → `products.id`

### `shipping_repayment_country_costs` {#table-shipping-repayment-country-costs}

| Column | Type |
|--------|------|
| `id` | serial |
| `shippingRepaymentConfigId` | integer |
| `countryId` | integer |
| `cost` | numeric(12, 2) |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `shippingRepaymentConfigId` → `shipping_repayment_config.id`
- `countryId` → `countries.id`

### `shipping_repayment_eligibility` {#table-shipping-repayment-eligibility}

| Column | Type |
|--------|------|
| `id` | serial |
| `shipmentItemId` | integer |
| `status` | shipping_repayment_eligibility_status_enum |
| `createdByAdminEmail` | character varying |
| `createdAt` | timestamp with time zone |
| `updatedAt` | timestamp with time zone |

**Foreign keys:**
- `shipmentItemId` → `shipment_items.id`

### `stores` {#table-stores}

| Column | Type |
|--------|------|
| `id` | serial |
| `countryId` | integer |
| `city` | character varying |
| `state` | character varying |
| `name` | character varying |
| `address` | character varying |
| `zipCode` | character varying |
| `pickupFee` | numeric |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `countryId` → `countries.id`

### `subproducts` {#table-subproducts}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | character varying |
| `sku` | character varying |
| `reference` | character varying |
| `metadata` | jsonb |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `comboProductId` | integer |
| `categoryId` | integer |
| `mainProductId` | integer |

**Foreign keys:**
- `comboProductId` → `products.id`
- `mainProductId` → `products.id`
- `categoryId` → `categories.id`

### `sync_service_queue_item` {#table-sync-service-queue-item}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `orderTransactionId` | integer |
| `status` | character varying |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `latestRequestBody` | jsonb |

**Foreign keys:**
- `orderTransactionId` → `order_transactions.id`

### `tags` {#table-tags}

| Column | Type |
|--------|------|
| `id` | serial |
| `name` | character varying |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

### `taxes` {#table-taxes}

| Column | Type |
|--------|------|
| `id` | serial |
| `countryId` | integer |
| `name` | character varying |
| `value` | integer |
| `type` | taxes_type_enum |
| `taxCategory` | taxes_taxcategory_enum |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |

**Foreign keys:**
- `countryId` → `countries.id`

### `typeORM_migrations` {#table-typeORM-migrations}

| Column | Type |
|--------|------|
| `id` | serial |
| `timestamp` | bigint |
| `name` | character varying |

### `typeorm_metadata` {#table-typeorm-metadata}

| Column | Type |
|--------|------|
| `type` | character varying |
| `database` | character varying |
| `schema` | character varying |
| `table` | character varying |
| `name` | character varying |
| `value` | text |

### `upgradable_items` {#table-upgradable-items}

| Column | Type |
|--------|------|
| `id` | uuid |
| `userBID` | character varying |
| `legacyOrderIdentifier` | character varying |
| `legacyOrderId` | integer |
| `upgradableItemIdentifier` | character varying |
| `legacyOrderItemId` | integer |
| `sku` | character varying |
| `legacySku` | character varying |
| `orderId` | character varying |
| `status` | character varying |
| `isShippingPaid` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `legacyOrderId` → `legacy_orders.id`
- `legacyOrderItemId` → `legacy_order_items.id`

### `upgrade_cart_assets` {#table-upgrade-cart-assets}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `assetOption` | jsonb |
| `calculatedCommision` | jsonb |
| `baseAssetName` | character varying |
| `baseAssetSymbol` | character varying |
| `baseAssetAmount` | numeric |
| `baseAssetPercentage` | numeric |
| `optionAssetName` | character varying |
| `optionAssetSymbol` | character varying |
| `optionAssetAmount` | numeric |
| `optionAssetPercentage` | numeric |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `cartId` → `upgrade_carts.id`

### `upgrade_cart_cashbacks` {#table-upgrade-cart-cashbacks}

| Column | Type |
|--------|------|
| `id` | serial |
| `upgradeCartId` | integer |
| `assetName` | character varying |
| `assetSymbol` | character varying |
| `cashbackAssetId` | integer |
| `totalAmount` | numeric |

**Foreign keys:**
- `cashbackAssetId` → `shipping_cashback_assets.id`
- `upgradeCartId` → `upgrade_carts.id`

### `upgrade_cart_fees` {#table-upgrade-cart-fees}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `feeName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | upgrade_cart_fees_type_enum |
| `feeCategory` | upgrade_cart_fees_feecategory_enum |

**Foreign keys:**
- `cartId` → `upgrade_carts.id`

### `upgrade_cart_products` {#table-upgrade-cart-products}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `upgradableItemIds` | text |
| `productId` | integer |
| `price` | numeric |
| `originalPrice` | numeric |
| `discount` | numeric |
| `quantity` | integer |
| `isEligibleForCommission` | boolean |
| `commission` | jsonb |
| `canProductBeRemoved` | boolean |
| `feedBackMessage` | character varying |
| `userPurchaseLimit` | integer |
| `canUserPurchaseTheProduct` | boolean |
| `totalOrderExistsForProduct` | integer |
| `maximumUserCanPurchase` | integer |
| `shippingItems` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `productId` → `products.id`
- `cartId` → `upgrade_carts.id`

### `upgrade_cart_taxes` {#table-upgrade-cart-taxes}

| Column | Type |
|--------|------|
| `id` | serial |
| `cartId` | integer |
| `taxName` | character varying |
| `amount` | numeric |
| `value` | numeric |
| `type` | upgrade_cart_taxes_type_enum |
| `taxCategory` | upgrade_cart_taxes_taxcategory_enum |

**Foreign keys:**
- `cartId` → `upgrade_carts.id`

### `upgrade_carts` {#table-upgrade-carts}

| Column | Type |
|--------|------|
| `id` | serial |
| `reference` | character varying |
| `cartState` | upgrade_carts_cartstate_enum |
| `userBID` | character varying |
| `billingAddressId` | integer |
| `shippingAddressId` | integer |
| `paymentMethodId` | integer |
| `shippingMethodId` | integer |
| `storeId` | integer |
| `commissionSubTotal` | numeric |
| `subTotal` | numeric |
| `feesTotal` | numeric |
| `discountTotal` | numeric |
| `vouchers` | jsonb |
| `shippingTotal` | numeric |
| `taxTotal` | numeric |
| `grandTotal` | numeric |
| `cartAssetId` | integer |
| `userSubscriptionType` | character varying |
| `isActive` | boolean |
| `isShippingApplicable` | boolean |
| `legacyOrderId` | character varying |
| `legacyOrderUniqueId` | integer |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `isSmartPay` | boolean |

**Foreign keys:**
- `shippingAddressId` → `user_addresses.id`
- `storeId` → `stores.id`
- `shippingMethodId` → `shipping_methods.id`
- `billingAddressId` → `user_addresses.id`
- `paymentMethodId` → `payment_methods.id`
- `cartAssetId` → `upgrade_cart_assets.id`

### `user_addresses` {#table-user-addresses}

| Column | Type |
|--------|------|
| `id` | serial |
| `userBID` | character varying |
| `firstName` | character varying |
| `lastName` | character varying |
| `phone` | character varying |
| `email` | character varying |
| `countryId` | integer |
| `countryCode` | character varying |
| `city` | character varying |
| `state` | character varying |
| `postalCode` | character varying |
| `address` | text |
| `latitude` | character varying |
| `longitude` | character varying |
| `type` | character varying |
| `isDefault` | boolean |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `deletedAt` | timestamp without time zone |
| `buildingInfo` | text |

**Foreign keys:**
- `countryId` → `countries.id`

### `user_payment_method_consents` {#table-user-payment-method-consents}

| Column | Type |
|--------|------|
| `id` | serial |
| `userId` | integer |
| `paymentMethodId` | integer |
| `accepted` | boolean |
| `acceptedAt` | timestamp without time zone |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `paymentMethodId` → `payment_methods.id`

### `users` {#table-users}

| Column | Type |
|--------|------|
| `id` | serial |
| `firstName` | text |
| `lastName` | text |
| `userName` | text |
| `bid` | text |
| `email` | text |
| `phone` | text |
| `countryId` | integer |
| `activeMembership` | boolean |
| `picture` | text |
| `profilePicture` | text |
| `originType` | text |
| `accountType` | text |
| `membershipExpiryDate` | timestamp without time zone |
| `isActive` | boolean |
| `isDeleted` | boolean |
| `kycActive` | boolean |
| `membershipExpiry` | boolean |
| `walletConsentConfirmed` | boolean |
| `walletConsentConfirmedDate` | timestamp without time zone |
| `kycDate` | timestamp without time zone |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |
| `dateJoined` | timestamp without time zone |
| `subscriptionType` | text |
| `downlineUsersCount` | integer |
| `hasActiveFirstLine` | boolean |
| `subscriptionActivationPending` | boolean |
| `isMemberShipPurchaseEligible` | boolean |

### `wallet_sequence_number` {#table-wallet-sequence-number}

| Column | Type |
|--------|------|
| `id` | serial |
| `createdFor` | character varying |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

### `xera_queue_item` {#table-xera-queue-item}

| Column | Type |
|--------|------|
| `id` | serial |
| `orderId` | character varying |
| `orderTransactionId` | integer |
| `status` | character varying |
| `latestRequestBody` | jsonb |
| `eventLogs` | jsonb |
| `createdAt` | timestamp without time zone |
| `updatedAt` | timestamp without time zone |

**Foreign keys:**
- `orderTransactionId` → `order_transactions.id`

---

## Foreign keys

| From table | Column | To table | To column |
|------------|--------|----------|-----------|
| `admin_activities` | `adminId` | `admins` | `id` |
| `admin_features` | `moduleId` | `admin_modules` | `id` |
| `admin_role_access` | `featureId` | `admin_features` | `id` |
| `admin_role_access` | `roleId` | `admin_roles` | `id` |
| `admins` | `roleId` | `admin_roles` | `id` |
| `cart_assets` | `cartId` | `carts` | `id` |
| `cart_fees` | `cartId` | `carts` | `id` |
| `cart_products` | `productId` | `products` | `id` |
| `cart_products` | `cartId` | `carts` | `id` |
| `cart_taxes` | `cartId` | `carts` | `id` |
| `carts` | `shippingAddressId` | `user_addresses` | `id` |
| `carts` | `paymentMethodId` | `payment_methods` | `id` |
| `carts` | `cartAssetId` | `cart_assets` | `id` |
| `carts` | `billingAddressId` | `user_addresses` | `id` |
| `connect_queue_item` | `orderTransactionId` | `order_transactions` | `id` |
| `country_cities` | `stateId` | `country_states` | `id` |
| `country_cities` | `countryId` | `countries` | `id` |
| `country_states` | `countryId` | `countries` | `id` |
| `credit_notes` | `orderId` | `orders` | `id` |
| `credit_notes` | `shipmentOrderId` | `shipment_orders` | `id` |
| `extension_cart_assets` | `cartId` | `extension_carts` | `id` |
| `extension_cart_cashbacks` | `extensionCartId` | `extension_carts` | `id` |
| `extension_cart_cashbacks` | `cashbackAssetId` | `shipping_cashback_assets` | `id` |
| `extension_cart_fees` | `cartId` | `extension_carts` | `id` |
| `extension_cart_products` | `orderUnitExtensionId` | `order_unit_extension_eligibilities` | `id` |
| `extension_cart_products` | `productId` | `products` | `id` |
| `extension_cart_products` | `cartId` | `extension_carts` | `id` |
| `extension_cart_taxes` | `cartId` | `extension_carts` | `id` |
| `extension_carts` | `paymentMethodId` | `payment_methods` | `id` |
| `extension_carts` | `billingAddressId` | `user_addresses` | `id` |
| `extension_carts` | `storeId` | `stores` | `id` |
| `extension_carts` | `shippingMethodId` | `shipping_methods` | `id` |
| `extension_carts` | `shippingAddressId` | `user_addresses` | `id` |
| `gen2_gen3_orders_migration_map` | `gen2OrderId` | `orders` | `id` |
| `gen2_gen3_orders_migration_map` | `gen3OrderId` | `orders` | `orderId` |
| `ioss_queue_item` | `orderTransactionId` | `order_transactions` | `id` |
| `legacy_order_items` | `orderId` | `legacy_orders` | `id` |
| `legacy_orders` | `invoiceId` | `order_invoices` | `id` |
| `machine_upgrade_queue_item` | `upgradableItemId` | `upgradable_items` | `id` |
| `migration_cart_assets` | `cartId` | `migration_carts` | `id` |
| `migration_cart_cashbacks` | `cashbackAssetId` | `shipping_cashback_assets` | `id` |
| `migration_cart_cashbacks` | `migrationCartId` | `migration_carts` | `id` |
| `migration_cart_fees` | `cartId` | `migration_carts` | `id` |
| `migration_cart_products` | `productId` | `products` | `id` |
| `migration_cart_products` | `cartId` | `migration_carts` | `id` |
| `migration_cart_products` | `shipmentItemId` | `shipment_items` | `id` |
| `migration_cart_products` | `gen2MigrationEligibilityId` | `gen2_migration_eligibility_v2` | `id` |
| `migration_cart_taxes` | `cartId` | `migration_carts` | `id` |
| `migration_carts` | `cartAssetId` | `migration_cart_assets` | `id` |
| `migration_carts` | `storeId` | `stores` | `id` |
| `migration_carts` | `shippingMethodId` | `shipping_methods` | `id` |
| `migration_carts` | `paymentMethodId` | `payment_methods` | `id` |
| `migration_carts` | `billingAddressId` | `user_addresses` | `id` |
| `migration_carts` | `shippingAddressId` | `user_addresses` | `id` |
| `migration_refund_request_items` | `shipmentCashbackQueueItemId` | `shipping_cashback_queue_item` | `id` |
| `migration_refund_request_items` | `migrationRefundRequestId` | `migration_refund_requests` | `id` |
| `migration_refund_requests` | `shipmentOrderId` | `shipment_orders` | `id` |
| `migration_refund_requests` | `gen2Gen3OrdersMigrationMapId` | `gen2_gen3_orders_migration_map` | `id` |
| `order_invoices` | `orderId` | `orders` | `id` |
| `order_item_units` | `orderItemId` | `order_items` | `id` |
| `order_items` | `orderId` | `orders` | `id` |
| `order_items` | `gen2MigrationEligibilityId` | `gen2_migration_eligibility_v2` | `id` |
| `order_items_v1` | `orderId` | `orders_v1` | `id` |
| `order_shipping_address_histories` | `orderInternalId` | `orders` | `id` |
| `order_transaction_v1` | `orderId` | `orders_v1` | `id` |
| `order_transactions` | `orderId` | `orders` | `id` |
| `order_unit_extension_eligibilities` | `extensionProductSku` | `products` | `sku` |
| `orders` | `invoiceId` | `order_invoices` | `id` |
| `orders_v1` | `invoiceId` | `order_invoices` | `id` |
| `partner_hub_bulk_address_verify_job_items` | `jobId` | `partner_hub_bulk_address_verify_jobs` | `id` |
| `payment_assets` | `paymentMethodId` | `payment_methods` | `id` |
| `payment_fees` | `paymentMethodId` | `payment_methods` | `id` |
| `payment_options` | `optionId` | `payment_assets` | `id` |
| `payment_options` | `fromAssetId` | `payment_assets` | `id` |
| `payment_restrictions` | `categoryId` | `categories` | `id` |
| `payment_restrictions` | `paymentOptionId` | `payment_options` | `id` |
| `payment_restrictions` | `productId` | `products` | `id` |
| `product_images` | `productFileId` | `product_files` | `id` |
| `product_images` | `productId` | `products` | `id` |
| `product_shipment_configurations` | `shippingMethodId` | `shipping_methods` | `id` |
| `product_shipment_configurations` | `productId` | `products` | `id` |
| `product_shipping_cashback_assets` | `cashbackAssetId` | `shipping_cashback_assets` | `id` |
| `product_shipping_cashback_assets` | `shippingMethodId` | `shipping_methods` | `id` |
| `product_shipping_costs` | `countryId` | `countries` | `id` |
| `product_shipping_costs` | `productId` | `products` | `id` |
| `product_shipping_costs` | `shippingProviderId` | `shipping_providers` | `id` |
| `product_shipping_costs` | `shippingMethodId` | `shipping_methods` | `id` |
| `product_tags` | `productId` | `products` | `id` |
| `product_tags` | `tagId` | `tags` | `id` |
| `product_upgrades` | `upgradableProductId` | `products` | `id` |
| `product_upgrades` | `upgradeProductId` | `products` | `id` |
| `products` | `categoryId` | `categories` | `id` |
| `shipment_item_logs` | `shipmentItemId` | `shipment_items` | `id` |
| `shipment_items` | `orderItemId` | `order_items` | `id` |
| `shipment_items` | `productId` | `products` | `id` |
| `shipment_items` | `shippingMethodId` | `shipping_methods` | `id` |
| `shipment_items` | `orderId` | `orders` | `id` |
| `shipment_items` | `pickupStoreId` | `stores` | `id` |
| `shipment_order_invoices` | `shipmentOrderId` | `shipment_orders` | `id` |
| `shipment_order_items` | `shipmentItemId` | `shipment_items` | `id` |
| `shipment_order_items` | `shipmentOrderId` | `shipment_orders` | `id` |
| `shipment_order_transactions` | `shipmentOrderId` | `shipment_orders` | `id` |
| `shipment_orders` | `orderUniqueId` | `orders` | `id` |
| `shipment_orders` | `shippingMethodId` | `shipping_methods` | `id` |
| `shipment_orders` | `shipmentInvoiceId` | `shipment_order_invoices` | `id` |
| `shipment_orders` | `storeId` | `stores` | `id` |
| `shipping_cart_assets` | `shippingCartId` | `shipping_carts` | `id` |
| `shipping_cart_cashbacks` | `shippingCartId` | `shipping_carts` | `id` |
| `shipping_cart_cashbacks` | `cashbackAssetId` | `shipping_cashback_assets` | `id` |
| `shipping_cart_fees` | `shippingCartId` | `shipping_carts` | `id` |
| `shipping_cart_products` | `shippingCartId` | `shipping_carts` | `id` |
| `shipping_cart_products` | `shipmentItemId` | `shipment_items` | `id` |
| `shipping_cart_taxes` | `shippingCartId` | `shipping_carts` | `id` |
| `shipping_carts` | `shippingMethodId` | `shipping_methods` | `id` |
| `shipping_carts` | `billingAddressId` | `user_addresses` | `id` |
| `shipping_carts` | `shippingCartAssetId` | `shipping_cart_assets` | `id` |
| `shipping_carts` | `paymentMethodId` | `payment_methods` | `id` |
| `shipping_carts` | `storeId` | `stores` | `id` |
| `shipping_carts` | `shippingAddressId` | `user_addresses` | `id` |
| `shipping_cashback_queue_item` | `ShipmentOrderTransactionId` | `shipment_order_transactions` | `id` |
| `shipping_providers` | `shippingMethodId` | `shipping_methods` | `id` |
| `shipping_repayment_config` | `productId` | `products` | `id` |
| `shipping_repayment_country_costs` | `shippingRepaymentConfigId` | `shipping_repayment_config` | `id` |
| `shipping_repayment_country_costs` | `countryId` | `countries` | `id` |
| `shipping_repayment_eligibility` | `shipmentItemId` | `shipment_items` | `id` |
| `stores` | `countryId` | `countries` | `id` |
| `subproducts` | `comboProductId` | `products` | `id` |
| `subproducts` | `mainProductId` | `products` | `id` |
| `subproducts` | `categoryId` | `categories` | `id` |
| `sync_service_queue_item` | `orderTransactionId` | `order_transactions` | `id` |
| `taxes` | `countryId` | `countries` | `id` |
| `upgradable_items` | `legacyOrderId` | `legacy_orders` | `id` |
| `upgradable_items` | `legacyOrderItemId` | `legacy_order_items` | `id` |
| `upgrade_cart_assets` | `cartId` | `upgrade_carts` | `id` |
| `upgrade_cart_cashbacks` | `cashbackAssetId` | `shipping_cashback_assets` | `id` |
| `upgrade_cart_cashbacks` | `upgradeCartId` | `upgrade_carts` | `id` |
| `upgrade_cart_fees` | `cartId` | `upgrade_carts` | `id` |
| `upgrade_cart_products` | `productId` | `products` | `id` |
| `upgrade_cart_products` | `cartId` | `upgrade_carts` | `id` |
| `upgrade_cart_taxes` | `cartId` | `upgrade_carts` | `id` |
| `upgrade_carts` | `shippingAddressId` | `user_addresses` | `id` |
| `upgrade_carts` | `storeId` | `stores` | `id` |
| `upgrade_carts` | `shippingMethodId` | `shipping_methods` | `id` |
| `upgrade_carts` | `billingAddressId` | `user_addresses` | `id` |
| `upgrade_carts` | `paymentMethodId` | `payment_methods` | `id` |
| `upgrade_carts` | `cartAssetId` | `upgrade_cart_assets` | `id` |
| `user_addresses` | `countryId` | `countries` | `id` |
| `user_payment_method_consents` | `paymentMethodId` | `payment_methods` | `id` |
| `xera_queue_item` | `orderTransactionId` | `order_transactions` | `id` |

---

## Support query patterns

### User by BID

```sql
SELECT * FROM users u
WHERE u.bid = %s
  AND (u."isDeleted" = false OR u."isDeleted" IS NULL);
```

### Orders by BID

```sql
SELECT o.id, o."orderId", o.status, o."paymentStatus", o."grandTotal", o."createdAt"
FROM orders o
WHERE o."userBID" = %s
  AND o."isDeleted" = false
ORDER BY o."createdAt" DESC
LIMIT 20;
```

### Order by public order ID with items

```sql
SELECT o.*, oi.name, oi.sku, oi.quantity, oi.price, oi.status
FROM orders o
JOIN order_items oi ON oi."orderId" = o.id
WHERE o."orderId" = %s;
```

### Identifier cheat sheet

| Customer says | Field | Table |
|---------------|-------|-------|
| BID | `bid` | `users` |
| BID (orders) | `userBID` | `orders`, `carts`, `user_addresses` |
| Order ID | `orderId` | `orders` |
| Internal id | `id` | any table (tools only) |
