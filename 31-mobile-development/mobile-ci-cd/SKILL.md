---
name: Mobile CI/CD Pipelines
description: Automating building, testing, and deploying mobile applications using GitHub Actions, Fastlane automation, code signing, and App Store submission automation.
---

# Mobile CI/CD Pipelines

> **Current Level:** Intermediate  
> **Domain:** Mobile Development / DevOps

---

## Overview

Mobile CI/CD automates building, testing, and deploying mobile applications. This guide covers GitHub Actions, Fastlane automation, code signing, and App Store submission automation for streamlining mobile app development and release processes.

---

## Core Concepts

### Table of Contents

1. [CI/CD for Mobile](#ci-cd-for-mobile)
2. [GitHub Actions for Mobile](#github-actions-for-mobile)
3. [Fastlane Automation](#fastlane-automation)
4. [Build Automation](#build-automation)
5. [Testing Automation](#testing-automation)
6. [Code Signing](#code-signing)
7. [Automated Deployment](#automated-deployment)
8. [App Store Submission Automation](#app-store-submission-automation)
9. [Version Management](#version-management)
10. [Release Notes Generation](#release-notes-generation)
11. [Monitoring Builds](#monitoring-builds)
12. [Best Practices](#best-practices)

---

## CI/CD for Mobile

### Mobile CI/CD Architecture

```yaml
# .github/workflows/mobile-ci-cd.yml
name: Mobile CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

jobs:
  # iOS jobs
  ios-test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd ios
          pod install

      - name: Run tests
        run: |
          xcodebuild test \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 14'

  ios-build:
    needs: ios-test
    runs-on: macos-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd ios
          pod install

      - name: Build iOS app
        run: |
          fastlane ios build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: ios-build
          path: ios/build/*.ipa

  ios-deploy:
    needs: ios-build
    runs-on: macos-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: ios-build

      - name: Deploy to TestFlight
        run: |
          fastlane ios testflight
        env:
          APP_STORE_CONNECT_API_KEY: ${{ secrets.APP_STORE_CONNECT_API_KEY }}

  # Android jobs
  android-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: |
          cd android
          ./gradlew test

      - name: Run lint
        run: |
          cd android
          ./gradlew lint

  android-build:
    needs: android-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Install dependencies
        run: npm install

      - name: Build Android app
        run: |
          fastlane android build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: android-build
          path: android/app/build/outputs/**/*.apk

  android-deploy:
    needs: android-build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: android-build

      - name: Deploy to Google Play
        run: |
          fastlane android internal
        env:
          GOOGLE_PLAY_SERVICE_ACCOUNT_JSON: ${{ secrets.GOOGLE_PLAY_SERVICE_ACCOUNT_JSON }}
```

---

## GitHub Actions for Mobile

### iOS Workflow

```yaml
# .github/workflows/ios.yml
name: iOS CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  release:
    types: [published]

env:
  XCODE_VERSION: '15.0'

jobs:
  test:
    runs-on: macos-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: ${{ env.XCODE_VERSION }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install CocoaPods
        run: |
          cd ios
          pod install

      - name: Run unit tests
        run: |
          xcodebuild test \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 14' \
            -enableCodeCoverage YES

      - name: Generate coverage report
        run: |
          xcrun xccov view --report --json DerivedData/Logs/Test/*.xcresult > coverage.json

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.json
          flags: ios

  build:
    needs: test
    runs-on: macos-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: ${{ env.XCODE_VERSION }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install CocoaPods
        run: |
          cd ios
          pod install

      - name: Build for testing
        run: |
          xcodebuild build-for-testing \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -destination 'generic/platform=iOS' \
            -configuration Release

      - name: Archive
        run: |
          xcodebuild archive \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -configuration Release \
            -archivePath build/MyApp.xcarchive \
            -allowProvisioningUpdates

      - name: Export IPA
        run: |
          xcodebuild -exportArchive \
            -archivePath build/MyApp.xcarchive \
            -exportPath build/export \
            -exportOptionsPlist ios/ExportOptions.plist

      - name: Upload IPA
        uses: actions/upload-artifact@v4
        with:
          name: MyApp-${{ github.sha }}.ipa
          path: build/export/*.ipa

  deploy-testflight:
    needs: build
    runs-on: macos-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: ${{ env.XCODE_VERSION }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Fastlane
        run: |
          brew install fastlane

      - name: Upload to TestFlight
        run: |
          cd ios
          fastlane testflight
        env:
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.APP_STORE_CONNECT_API_KEY_ID }}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.APP_STORE_CONNECT_API_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{ secrets.APP_STORE_CONNECT_API_KEY_CONTENT }}
```

### Android Workflow

```yaml
# .github/workflows/android.yml
name: Android CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  release:
    types: [published]

env:
  JAVA_VERSION: '17'
  JAVA_DISTRIBUTION: 'temurin'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: ${{ env.JAVA_DISTRIBUTION }}
          java-version: ${{ env.JAVA_VERSION }}

      - name: Install dependencies
        run: npm ci

      - name: Cache Gradle
        uses: actions/cache@v3
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            ${{ runner.os }}-gradle-

      - name: Run unit tests
        run: |
          cd android
          ./gradlew test

      - name: Run instrumentation tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          target: google_apis
          arch: x86_64
          script: cd android && ./gradlew connectedCheck

      - name: Run lint
        run: |
          cd android
          ./gradlew lint

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: android-test-results
          path: android/app/build/test-results/

      - name: Upload lint results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: android-lint-results
          path: android/app/build/reports/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: ${{ env.JAVA_DISTRIBUTION }}
          java-version: ${{ env.JAVA_VERSION }}

      - name: Install dependencies
        run: npm ci

      - name: Cache Gradle
        uses: actions/cache@v3
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            ${{ runner.os }}-gradle-

      - name: Build release APK
        run: |
          cd android
          ./gradlew assembleRelease

      - name: Build release AAB
        run: |
          cd android
          ./gradlew bundleRelease

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: MyApp-${{ github.sha }}.apk
          path: android/app/build/outputs/apk/release/*.apk

      - name: Upload AAB
        uses: actions/upload-artifact@v4
        with:
          name: MyApp-${{ github.sha }}.aab
          path: android/app/build/outputs/bundle/release/*.aab

  deploy-internal:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: ${{ env.JAVA_DISTRIBUTION }}
          java-version: ${{ env.JAVA_VERSION }}

      - name: Install dependencies
        run: npm ci

      - name: Install Fastlane
        run: |
          sudo gem install fastlane

      - name: Upload to Google Play Internal Testing
        run: |
          cd android
          fastlane internal
        env:
          GOOGLE_PLAY_SERVICE_ACCOUNT_JSON: ${{ secrets.GOOGLE_PLAY_SERVICE_ACCOUNT_JSON }}

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: ${{ env.JAVA_DISTRIBUTION }}
          java-version: ${{ env.JAVA_VERSION }}

      - name: Install dependencies
        run: npm ci

      - name: Install Fastlane
        run: |
          sudo gem install fastlane

      - name: Upload to Google Play Production
        run: |
          cd android
          fastlane production
        env:
          GOOGLE_PLAY_SERVICE_ACCOUNT_JSON: ${{ secrets.GOOGLE_PLAY_SERVICE_ACCOUNT_JSON }}
```

---

## Fastlane Automation

### Fastlane Configuration

```ruby
# fastlane/Fastfile

default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      devices: ["iPhone 14"],
      code_coverage: true
    )
  end

  desc "Build app"
  lane :build do
    increment_build_number

    match(
      type: "appstore",
      readonly: true
    )

    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )
  end

  desc "Submit to TestFlight"
  lane :testflight do
    increment_build_number

    match(
      type: "appstore",
      readonly: true
    )

    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )

    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      changelog: "Bug fixes and improvements"
    )
  end

  desc "Submit to App Store"
  lane :release do
    increment_build_number

    match(
      type: "appstore",
      readonly: true
    )

    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )

    upload_to_app_store(
      submit_for_review: true,
      automatic_release: false,
      force: true,
      submission_information: {
        add_id_info_uses_idfa: false
      },
      app_rating_config_path: "./fastlane/metadata/app_rating_config.json"
    )
  end

  desc "Generate screenshots"
  lane :screenshots do
    capture_screenshots(
      scheme: "MyApp",
      devices: [
        "iPhone 14 Pro Max",
        "iPhone 14 Pro",
        "iPhone 14",
        "iPad Pro (12.9-inch) (6th generation)"
      ],
      languages: ["en-US", "es-ES", "fr-FR"],
      clear_previous_screenshots: true
    )

    frame_screenshots(
      white: true
    )
  end

  desc "Update metadata"
  lane :metadata do
    upload_to_app_store(
      skip_binary_upload: true,
      skip_screenshots: false,
      skip_metadata: false
    )
  end
end

platform :android do
  desc "Run tests"
  lane :test do
    gradle(
      task: "test",
      project_dir: "android/"
    )
  end

  desc "Build app"
  lane :build do
    gradle(
      task: "assemble",
      build_type: "Release",
      project_dir: "android/"
    )
  end

  desc "Submit to Google Play Internal Testing"
  lane :internal do
    gradle(
      task: "assemble",
      build_type: "Release",
      project_dir: "android/"
    )

    upload_to_play_store(
      track: "internal",
      aab: "./android/app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: false,
      skip_upload_images: false,
      skip_upload_screenshots: false,
      skip_upload_changelogs: false
    )
  end

  desc "Submit to Google Play Production"
  lane :production do
    gradle(
      task: "bundle",
      build_type: "Release",
      project_dir: "android/"
    )

    upload_to_play_store(
      track: "production",
      aab: "./android/app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: false,
      skip_upload_images: false,
      skip_upload_screenshots: false,
      skip_upload_changelogs: false,
      release_status: "completed",
      rollout: "0.1" # 10% staged rollout
    )
  end

  desc "Generate screenshots"
  lane :screenshots do
    capture_android_screenshots(
      locales: ["en-US", "es-ES", "fr-FR"],
      clear_previous_screenshots: true
    )
  end

  desc "Update metadata"
  lane :metadata do
    upload_to_play_store(
      track: "production",
      skip_upload_apk: true,
      skip_upload_aab: true,
      skip_upload_metadata: false,
      skip_upload_images: false,
      skip_upload_screenshots: false,
      skip_upload_changelogs: false
    )
  end
end
```

---

## Build Automation

### Build Script

```typescript
// scripts/build.ts
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

interface BuildConfig {
  platform: 'ios' | 'android';
  environment: 'development' | 'staging' | 'production';
  version?: string;
  buildNumber?: number;
}

class BuildManager {
  /**
   * Build app
   */
  async build(config: BuildConfig): Promise<void> {
    console.log(`Building ${config.platform} app for ${config.environment}...`);

    // Update version if provided
    if (config.version) {
      await this.updateVersion(config.platform, config.version, config.buildNumber);
    }

    // Run tests
    await this.runTests(config.platform);

    // Build app
    switch (config.platform) {
      case 'ios':
        await this.buildIOS(config.environment);
        break;
      case 'android':
        await this.buildAndroid(config.environment);
        break;
    }

    console.log(`Build completed successfully!`);
  }

  /**
   * Update version
   */
  private async updateVersion(
    platform: 'ios' | 'android',
    version: string,
    buildNumber?: number
  ): Promise<void> {
    const packageJsonPath = resolve('package.json');
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));

    packageJson.version = version;
    writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));

    if (platform === 'ios') {
      const plistPath = resolve('ios/MyApp/Info.plist');
      let plist = readFileSync(plistPath, 'utf-8');

      plist = plist.replace(
        /<key>CFBundleShortVersionString<\/key>\s*<string>.*<\/string>/,
        `<key>CFBundleShortVersionString</key>\n\t<string>${version}</string>`
      );

      if (buildNumber) {
        plist = plist.replace(
          /<key>CFBundleVersion<\/key>\s*<string>.*<\/string>/,
          `<key>CFBundleVersion</key>\n\t<string>${buildNumber}</string>`
        );
      }

      writeFileSync(plistPath, plist);
    } else {
      const gradlePath = resolve('android/app/build.gradle');
      let gradle = readFileSync(gradlePath, 'utf-8');

      gradle = gradle.replace(
        /versionName ".*"/,
        `versionName "${version}"`
      );

      if (buildNumber) {
        gradle = gradle.replace(
          /versionCode \d+/,
          `versionCode ${buildNumber}`
        );
      }

      writeFileSync(gradlePath, gradle);
    }
  }

  /**
   * Run tests
   */
  private async runTests(platform: 'ios' | 'android'): Promise<void> {
    console.log(`Running ${platform} tests...`);

    switch (platform) {
      case 'ios':
        execSync('fastlane ios test', { stdio: 'inherit' });
        break;
      case 'android':
        execSync('fastlane android test', { stdio: 'inherit' });
        break;
    }
  }

  /**
   * Build iOS
   */
  private async buildIOS(environment: string): Promise<void> {
    console.log(`Building iOS app for ${environment}...`);

    const scheme = environment === 'production' ? 'MyApp' : `MyApp-${environment}`;

    execSync(`fastlane ios build scheme:${scheme}`, { stdio: 'inherit' });
  }

  /**
   * Build Android
   */
  private async buildAndroid(environment: string): Promise<void> {
    console.log(`Building Android app for ${environment}...`);

    const buildType = environment === 'production' ? 'Release' : environment;

    execSync(`fastlane android build buildType:${buildType}`, { stdio: 'inherit' });
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: BuildConfig = {
    platform: args[0] as 'ios' | 'android',
    environment: args[1] as 'development' | 'staging' | 'production',
    version: args[2],
    buildNumber: args[3] ? parseInt(args[3]) : undefined,
  };

  const buildManager = new BuildManager();
  await buildManager.build(config);
}

main().catch(console.error);
```

---

## Testing Automation

### Test Runner

```typescript
// scripts/test.ts
import { execSync } from 'child_process';

interface TestConfig {
  platform: 'ios' | 'android';
  type: 'unit' | 'integration' | 'e2e';
  coverage?: boolean;
}

class TestRunner {
  /**
   * Run tests
   */
  async runTests(config: TestConfig): Promise<void> {
    console.log(`Running ${config.type} tests for ${config.platform}...`);

    switch (config.platform) {
      case 'ios':
        await this.runIOSTests(config);
        break;
      case 'android':
        await this.runAndroidTests(config);
        break;
    }

    console.log(`Tests completed successfully!`);
  }

  /**
   * Run iOS tests
   */
  private async runIOSTests(config: TestConfig): Promise<void> {
    switch (config.type) {
      case 'unit':
        execSync('xcodebuild test -workspace MyApp.xcworkspace -scheme MyApp -destination \'platform=iOS Simulator,name=iPhone 14\' -enableCodeCoverage YES', { stdio: 'inherit' });
        break;
      case 'integration':
        execSync('xcodebuild test -workspace MyApp.xcworkspace -scheme MyApp -destination \'platform=iOS Simulator,name=iPhone 14\' -only-testing:MyAppTests/IntegrationTests', { stdio: 'inherit' });
        break;
      case 'e2e':
        execSync('detox test --configuration ios.sim.release', { stdio: 'inherit' });
        break;
    }

    if (config.coverage) {
      this.generateCoverageReport('ios');
    }
  }

  /**
   * Run Android tests
   */
  private async runAndroidTests(config: TestConfig): Promise<void> {
    switch (config.type) {
      case 'unit':
        execSync('cd android && ./gradlew test', { stdio: 'inherit' });
        break;
      case 'integration':
        execSync('cd android && ./gradlew connectedAndroidTest', { stdio: 'inherit' });
        break;
      case 'e2e':
        execSync('detox test --configuration android.emu.release', { stdio: 'inherit' });
        break;
    }

    if (config.coverage) {
      this.generateCoverageReport('android');
    }
  }

  /**
   * Generate coverage report
   */
  private generateCoverageReport(platform: 'ios' | 'android'): void {
    console.log(`Generating ${platform} coverage report...`);

    switch (platform) {
      case 'ios':
        execSync('xcrun xccov view --report --json DerivedData/Logs/Test/*.xcresult > coverage.json', { stdio: 'inherit' });
        break;
      case 'android':
        execSync('cd android && ./gradlew jacocoTestReport', { stdio: 'inherit' });
        break;
    }
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: TestConfig = {
    platform: args[0] as 'ios' | 'android',
    type: args[1] as 'unit' | 'integration' | 'e2e',
    coverage: args.includes('--coverage'),
  };

  const testRunner = new TestRunner();
  await testRunner.runTests(config);
}

main().catch(console.error);
```

---

## Code Signing

### Code Signing Manager

```typescript
// scripts/sign.ts
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

interface SigningConfig {
  platform: 'ios' | 'android';
  environment: 'development' | 'staging' | 'production';
}

class SigningManager {
  /**
   * Setup code signing
   */
  async setupSigning(config: SigningConfig): Promise<void> {
    console.log(`Setting up ${config.platform} code signing for ${config.environment}...`);

    switch (config.platform) {
      case 'ios':
        await this.setupIOSSigning(config.environment);
        break;
      case 'android':
        await this.setupAndroidSigning(config.environment);
        break;
    }

    console.log(`Code signing setup completed!`);
  }

  /**
   * Setup iOS signing
   */
  private async setupIOSSigning(environment: string): Promise<void> {
    const type = environment === 'production' ? 'appstore' : 'development';

    execSync(`fastlane match type:${type} readonly:true`, { stdio: 'inherit' });
  }

  /**
   * Setup Android signing
   */
  private async setupAndroidSigning(environment: string): Promise<void> {
    const keystorePath = resolve('android/app/keystore.jks');
    const keystorePropertiesPath = resolve('android/keystore.properties');

    // Check if keystore exists
    if (!require('fs').existsSync(keystorePath)) {
      console.log('Keystore not found. Please create one manually.');
      return;
    }

    // Read keystore properties
    const keystoreProperties = readFileSync(keystorePropertiesPath, 'utf-8');

    // Update build.gradle
    const gradlePath = resolve('android/app/build.gradle');
    let gradle = readFileSync(gradlePath, 'utf-8');

    // Add signing config
    if (!gradle.includes('signingConfigs')) {
      gradle = gradle.replace(
        /android {/,
        `android {\n    signingConfigs {\n        release {\n            storeFile file(keystoreProperties['storeFile'])\n            storePassword keystoreProperties['storePassword']\n            keyAlias keystoreProperties['keyAlias']\n            keyPassword keystoreProperties['keyPassword']\n        }\n    }`
      );
    }

    // Add signing config to build type
    gradle = gradle.replace(
      /buildTypes {\s*release {/,
      `buildTypes {\n        release {\n            signingConfig signingConfigs.release`
    );

    writeFileSync(gradlePath, gradle);
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: SigningConfig = {
    platform: args[0] as 'ios' | 'android',
    environment: args[1] as 'development' | 'staging' | 'production',
  };

  const signingManager = new SigningManager();
  await signingManager.setupSigning(config);
}

main().catch(console.error);
```

---

## Automated Deployment

### Deployment Manager

```typescript
// scripts/deploy.ts
import { execSync } from 'child_process';

interface DeploymentConfig {
  platform: 'ios' | 'android';
  environment: 'testflight' | 'beta' | 'production';
  changelog?: string;
}

class DeploymentManager {
  /**
   * Deploy app
   */
  async deploy(config: DeploymentConfig): Promise<void> {
    console.log(`Deploying ${config.platform} app to ${config.environment}...`);

    switch (config.platform) {
      case 'ios':
        await this.deployIOS(config);
        break;
      case 'android':
        await this.deployAndroid(config);
        break;
    }

    console.log(`Deployment completed successfully!`);
  }

  /**
   * Deploy iOS
   */
  private async deployIOS(config: DeploymentConfig): Promise<void> {
    const changelog = config.changelog || 'Bug fixes and improvements';

    switch (config.environment) {
      case 'testflight':
        execSync(`fastlane ios testflight changelog:"${changelog}"`, { stdio: 'inherit' });
        break;
      case 'production':
        execSync(`fastlane ios release changelog:"${changelog}"`, { stdio: 'inherit' });
        break;
    }
  }

  /**
   * Deploy Android
   */
  private async deployAndroid(config: DeploymentConfig): Promise<void> {
    const changelog = config.changelog || 'Bug fixes and improvements';

    switch (config.environment) {
      case 'beta':
        execSync(`fastlane android internal changelog:"${changelog}"`, { stdio: 'inherit' });
        break;
      case 'production':
        execSync(`fastlane android production changelog:"${changelog}"`, { stdio: 'inherit' });
        break;
    }
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: DeploymentConfig = {
    platform: args[0] as 'ios' | 'android',
    environment: args[1] as 'testflight' | 'beta' | 'production',
    changelog: args[2],
  };

  const deploymentManager = new DeploymentManager();
  await deploymentManager.deploy(config);
}

main().catch(console.error);
```

---

## App Store Submission Automation

### Submission Manager

```typescript
// scripts/submit.ts
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

interface SubmissionConfig {
  platform: 'ios' | 'android';
  environment: 'testflight' | 'beta' | 'production';
  version: string;
  changelog: string;
}

class SubmissionManager {
  /**
   * Submit app
   */
  async submit(config: SubmissionConfig): Promise<void> {
    console.log(`Submitting ${config.platform} app ${config.version} to ${config.environment}...`);

    // Update version
    await this.updateVersion(config.platform, config.version);

    // Build app
    await this.buildApp(config.platform, config.environment);

    // Submit to store
    await this.submitToStore(config);

    console.log(`Submission completed successfully!`);
  }

  /**
   * Update version
   */
  private async updateVersion(
    platform: 'ios' | 'android',
    version: string
  ): Promise<void> {
    const packageJsonPath = resolve('package.json');
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));

    packageJson.version = version;
    writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
  }

  /**
   * Build app
   */
  private async buildApp(
    platform: 'ios' | 'android',
    environment: string
  ): Promise<void> {
    switch (platform) {
      case 'ios':
        execSync('fastlane ios build', { stdio: 'inherit' });
        break;
      case 'android':
        execSync('fastlane android build', { stdio: 'inherit' });
        break;
    }
  }

  /**
   * Submit to store
   */
  private async submitToStore(config: SubmissionConfig): Promise<void> {
    switch (config.platform) {
      case 'ios':
        await this.submitIOS(config);
        break;
      case 'android':
        await this.submitAndroid(config);
        break;
    }
  }

  /**
   * Submit iOS
   */
  private async submitIOS(config: SubmissionConfig): Promise<void> {
    switch (config.environment) {
      case 'testflight':
        execSync(`fastlane ios testflight changelog:"${config.changelog}"`, { stdio: 'inherit' });
        break;
      case 'production':
        execSync(`fastlane ios release changelog:"${config.changelog}"`, { stdio: 'inherit' });
        break;
    }
  }

  /**
   * Submit Android
   */
  private async submitAndroid(config: SubmissionConfig): Promise<void> {
    switch (config.environment) {
      case 'beta':
        execSync(`fastlane android internal changelog:"${config.changelog}"`, { stdio: 'inherit' });
        break;
      case 'production':
        execSync(`fastlane android production changelog:"${config.changelog}"`, { stdio: 'inherit' });
        break;
    }
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: SubmissionConfig = {
    platform: args[0] as 'ios' | 'android',
    environment: args[1] as 'testflight' | 'beta' | 'production',
    version: args[2],
    changelog: args[3],
  };

  const submissionManager = new SubmissionManager();
  await submissionManager.submit(config);
}

main().catch(console.error);
```

---

## Version Management

### Version Manager

```typescript
// scripts/version.ts
import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

interface VersionConfig {
  type: 'major' | 'minor' | 'patch';
  platform: 'ios' | 'android';
}

class VersionManager {
  /**
   * Bump version
   */
  async bumpVersion(config: VersionConfig): Promise<string> {
    const packageJsonPath = resolve('package.json');
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));

    const currentVersion = packageJson.version;
    const newVersion = this.incrementVersion(currentVersion, config.type);

    console.log(`Bumping version from ${currentVersion} to ${newVersion}...`);

    // Update package.json
    packageJson.version = newVersion;
    writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));

    // Update platform-specific version
    await this.updatePlatformVersion(config.platform, newVersion);

    console.log(`Version bumped to ${newVersion}!`);

    return newVersion;
  }

  /**
   * Increment version
   */
  private incrementVersion(
    version: string,
    type: 'major' | 'minor' | 'patch'
  ): string {
    const [major, minor, patch] = version.split('.').map(Number);

    switch (type) {
      case 'major':
        return `${major + 1}.0.0`;
      case 'minor':
        return `${major}.${minor + 1}.0`;
      case 'patch':
        return `${major}.${minor}.${patch + 1}`;
      default:
        return version;
    }
  }

  /**
   * Update platform version
   */
  private async updatePlatformVersion(
    platform: 'ios' | 'android',
    version: string
  ): Promise<void> {
    switch (platform) {
      case 'ios':
        await this.updateIOSVersion(version);
        break;
      case 'android':
        await this.updateAndroidVersion(version);
        break;
    }
  }

  /**
   * Update iOS version
   */
  private async updateIOSVersion(version: string): Promise<void> {
    const plistPath = resolve('ios/MyApp/Info.plist');
    let plist = readFileSync(plistPath, 'utf-8');

    plist = plist.replace(
      /<key>CFBundleShortVersionString<\/key>\s*<string>.*<\/string>/,
      `<key>CFBundleShortVersionString</key>\n\t<string>${version}</string>`
    );

    writeFileSync(plistPath, plist);
  }

  /**
   * Update Android version
   */
  private async updateAndroidVersion(version: string): Promise<void> {
    const gradlePath = resolve('android/app/build.gradle');
    let gradle = readFileSync(gradlePath, 'utf-8');

    gradle = gradle.replace(
      /versionName ".*"/,
      `versionName "${version}"`
    );

    writeFileSync(gradlePath, gradle);
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: VersionConfig = {
    type: args[0] as 'major' | 'minor' | 'patch',
    platform: args[1] as 'ios' | 'android',
  };

  const versionManager = new VersionManager();
  await versionManager.bumpVersion(config);
}

main().catch(console.error);
```

---

## Release Notes Generation

### Release Notes Generator

```typescript
// scripts/release-notes.ts
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

interface ReleaseNotesConfig {
  version: string;
  previousVersion?: string;
}

class ReleaseNotesGenerator {
  /**
   * Generate release notes
   */
  async generateReleaseNotes(config: ReleaseNotesConfig): Promise<string> {
    console.log(`Generating release notes for version ${config.version}...`);

    const commits = await this.getCommits(config.previousVersion);
    const categorizedCommits = this.categorizeCommits(commits);
    const releaseNotes = this.formatReleaseNotes(config.version, categorizedCommits);

    console.log(`Release notes generated!`);

    return releaseNotes;
  }

  /**
   * Get commits
   */
  private async getCommits(fromVersion?: string): Promise<string[]> {
    let command = 'git log --pretty=format:"%s"';

    if (fromVersion) {
      command += ` ${fromVersion}..HEAD`;
    }

    const output = execSync(command, { encoding: 'utf-8' });

    return output.split('\n').filter(Boolean);
  }

  /**
   * Categorize commits
   */
  private categorizeCommits(commits: string[]): {
    features: string[];
    fixes: string[];
    others: string[];
  } {
    const features: string[] = [];
    const fixes: string[] = [];
    const others: string[] = [];

    for (const commit of commits) {
      if (commit.startsWith('feat:')) {
        features.push(commit.replace('feat:', '').trim());
      } else if (commit.startsWith('fix:')) {
        fixes.push(commit.replace('fix:', '').trim());
      } else {
        others.push(commit);
      }
    }

    return { features, fixes, others };
  }

  /**
   * Format release notes
   */
  private formatReleaseNotes(
    version: string,
    categorized: {
      features: string[];
      fixes: string[];
      others: string[];
    }
  ): string {
    const notes = [
      `# Release ${version}`,
      '',
      `## Date`,
      new Date().toISOString().split('T')[0],
      '',
    ];

    if (categorized.features.length > 0) {
      notes.push('## Features');
      for (const feature of categorized.features) {
        notes.push(`- ${feature}`);
      }
      notes.push('');
    }

    if (categorized.fixes.length > 0) {
      notes.push('## Bug Fixes');
      for (const fix of categorized.fixes) {
        notes.push(`- ${fix}`);
      }
      notes.push('');
    }

    if (categorized.others.length > 0) {
      notes.push('## Other Changes');
      for (const other of categorized.others) {
        notes.push(`- ${other}`);
      }
      notes.push('');
    }

    return notes.join('\n');
  }

  /**
   * Save release notes
   */
  async saveReleaseNotes(version: string, notes: string): Promise<void> {
    const releaseNotesPath = resolve('RELEASE_NOTES', `${version}.md`);

    writeFileSync(releaseNotesPath, notes);

    console.log(`Release notes saved to ${releaseNotesPath}`);
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: ReleaseNotesConfig = {
    version: args[0],
    previousVersion: args[1],
  };

  const generator = new ReleaseNotesGenerator();
  const notes = await generator.generateReleaseNotes(config);
  await generator.saveReleaseNotes(config.version, notes);

  console.log('\n' + notes);
}

main().catch(console.error);
```

---

## Monitoring Builds

### Build Monitor

```typescript
// scripts/monitor.ts
import { execSync } from 'child_process';

interface BuildMonitorConfig {
  platform: 'ios' | 'android';
  environment: 'development' | 'staging' | 'production';
}

class BuildMonitor {
  /**
   * Monitor build
   */
  async monitor(config: BuildMonitorConfig): Promise<void> {
    console.log(`Monitoring ${config.platform} ${config.environment} build...`);

    // Get build status
    const status = await this.getBuildStatus(config);

    console.log(`Build status: ${status}`);

    // Check for errors
    if (status === 'failed') {
      const errors = await this.getBuildErrors(config);

      console.log('\nBuild errors:');
      for (const error of errors) {
        console.log(`- ${error}`);
      }
    }

    // Get build metrics
    const metrics = await this.getBuildMetrics(config);

    console.log('\nBuild metrics:');
    console.log(`- Duration: ${metrics.duration}s`);
    console.log(`- Size: ${metrics.size}MB`);
    console.log(`- Tests: ${metrics.testsPassed}/${metrics.testsTotal}`);
  }

  /**
   * Get build status
   */
  private async getBuildStatus(config: BuildMonitorConfig): Promise<string> {
    // Implement based on CI/CD platform
    return 'success';
  }

  /**
   * Get build errors
   */
  private async getBuildErrors(config: BuildMonitorConfig): Promise<string[]> {
    // Implement based on CI/CD platform
    return [];
  }

  /**
   * Get build metrics
   */
  private async getBuildMetrics(config: BuildMonitorConfig): Promise<{
    duration: number;
    size: number;
    testsPassed: number;
    testsTotal: number;
  }> {
    // Implement based on CI/CD platform
    return {
      duration: 120,
      size: 50,
      testsPassed: 100,
      testsTotal: 100,
    };
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  const config: BuildMonitorConfig = {
    platform: args[0] as 'ios' | 'android',
    environment: args[1] as 'development' | 'staging' | 'production',
  };

  const monitor = new BuildMonitor();
  await monitor.monitor(config);
}

main().catch(console.error);
```

---

## Best Practices

### CI/CD Best Practices

```typescript
// 1. Use environment-specific configurations
const getBuildConfig = (environment: string) => {
  const configs: Record<string, any> = {
    development: {
      apiUrl: 'https://dev-api.example.com',
      analyticsEnabled: false,
      debugMode: true,
    },
    staging: {
      apiUrl: 'https://staging-api.example.com',
      analyticsEnabled: true,
      debugMode: true,
    },
    production: {
      apiUrl: 'https://api.example.com',
      analyticsEnabled: true,
      debugMode: false,
    },
  };

  return configs[environment] || configs.development;
};

// 2. Run tests before deployment
const runTestsBeforeDeploy = async (platform: 'ios' | 'android') => {
  console.log(`Running ${platform} tests...`);

  try {
    execSync(`fastlane ${platform} test`, { stdio: 'inherit' });
    console.log('Tests passed!');
  } catch (error) {
    console.error('Tests failed!');
    process.exit(1);
  }
};

// 3. Use semantic versioning
const getSemanticVersion = (changes: {
  breaking: number;
  features: number;
  fixes: number;
}): string => {
  const packageJson = JSON.parse(readFileSync('package.json', 'utf-8'));
  const [major, minor, patch] = packageJson.version.split('.').map(Number);

  if (changes.breaking > 0) {
    return `${major + 1}.0.0`;
  } else if (changes.features > 0) {
    return `${major}.${minor + 1}.0`;
  } else if (changes.fixes > 0) {
    return `${major}.${minor}.${patch + 1}`;
  }

  return packageJson.version;
};

// 4. Use staged rollouts
const deployWithStagedRollout = async (platform: 'ios' | 'android') => {
  const rolloutSchedule = [
    { percentage: 0.1, delay: 24 }, // 10% after 24 hours
    { percentage: 0.5, delay: 48 }, // 50% after 48 hours
    { percentage: 1.0, delay: 72 }, // 100% after 72 hours
  ];

  for (const schedule of rolloutSchedule) {
    console.log(`Rolling out to ${schedule.percentage * 100}%...`);

    // Deploy to percentage
    if (platform === 'android') {
      execSync(`fastlane android rollout rollout:${schedule.percentage}`, { stdio: 'inherit' });
    }

    // Wait for next rollout
    await new Promise(resolve => setTimeout(resolve, schedule.delay * 60 * 60 * 1000));
  }
};

// 5. Monitor builds and roll back if needed
const monitorAndRollback = async (platform: 'ios' | 'android') => {
  const metrics = await getBuildMetrics(platform);

  if (metrics.crashRate > 0.05) {
    console.error('High crash rate detected! Rolling back...');
    await rollback(platform);
  }
};
```

---

---

## Quick Start

### Fastlane Setup

```ruby
# Fastfile
platform :ios do
  lane :beta do
    increment_build_number
    build_app(scheme: "MyApp")
    upload_to_testflight
  end
  
  lane :release do
    increment_build_number
    build_app(scheme: "MyApp")
    upload_to_app_store
  end
end

platform :android do
  lane :beta do
    gradle(task: "assembleRelease")
    upload_to_play_store(track: "internal")
  end
end
```

### GitHub Actions

```yaml
name: Mobile CI/CD

on:
  push:
    branches: [main]

jobs:
  ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Fastlane
        run: bundle install
      - name: Build and Deploy
        run: fastlane beta
```

---

## Production Checklist

- [ ] **CI/CD Setup**: GitHub Actions or similar configured
- [ ] **Fastlane**: Fastlane automation set up
- [ ] **Code Signing**: Automated code signing
- [ ] **Build Automation**: Automated builds
- [ ] **Testing**: Automated testing in CI
- [ ] **App Store**: Automated App Store submission
- [ ] **Version Management**: Automated versioning
- [ ] **Release Notes**: Automated release notes
- [ ] **Monitoring**: Monitor build status
- [ ] **Secrets**: Secure secrets management
- [ ] **Documentation**: Document CI/CD process
- [ ] **Rollback**: Rollback procedures

---

## Anti-patterns

### ❌ Don't: Manual Builds

```markdown
# ❌ Bad - Manual process
1. Build locally
2. Upload to TestFlight
3. Wait for processing
4. Submit for review
# Slow and error-prone!
```

```markdown
# ✅ Good - Automated
git push → CI builds → Auto-deploy to TestFlight
# Fast and reliable
```

### ❌ Don't: Expose Secrets

```yaml
# ❌ Bad - Secrets in code
env:
  APP_STORE_API_KEY: "abc123"  # Exposed!
```

```yaml
# ✅ Good - GitHub Secrets
env:
  APP_STORE_API_KEY: ${{ secrets.APP_STORE_API_KEY }}
```

---

## Integration Points

- **App Distribution** (`31-mobile-development/app-distribution/`) - Distribution process
- **React Native Patterns** (`31-mobile-development/react-native-patterns/`) - App patterns
- **CI/CD** (`15-devops-infrastructure/ci-cd-github-actions/`) - CI/CD patterns

---

## Further Reading

- [Fastlane Documentation](https://docs.fastlane.tools/)
- [GitHub Actions for Mobile](https://github.com/actions/virtual-environments)
- [Mobile CI/CD Best Practices](https://www.raywenderlich.com/books/fastlane-tutorial)

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Fastlane Documentation](https://docs.fastlane.tools/)
- [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
- [Google Play Developer API](https://developers.google.com/android-publisher)
- [React Native CodePush](https://microsoft.github.io/code-push/)
