---
name: React Native Development Patterns
description: Project structure, navigation, state management, styling, and best practices for building cross-platform mobile applications with React Native.
---

# React Native Development Patterns

> **Current Level:** Intermediate  
> **Domain:** Mobile Development / Frontend

---

## Overview

React Native development patterns cover project structure, navigation, state management, styling, and best practices for building cross-platform mobile applications. Effective React Native development uses platform-specific optimizations, proper state management, and native module integration to create performant mobile apps.

---

---

## Core Concepts

### Table of Contents

1. [React Native Setup](#react-native-setup)
2. [Project Structure](#project-structure)
3. [Navigation](#navigation)
4. [State Management](#state-management)
5. [Styling Patterns](#styling-patterns)
6. [Platform-Specific Code](#platform-specific-code)
7. [Native Modules](#native-modules)
8. [Performance Optimization](#performance-optimization)
9. [Image Handling](#image-handling)
10. [Offline Support](#offline-support)
11. [Debugging](#debugging)
12. [Testing](#testing)
13. [Common Libraries](#common-libraries)
14. [Best Practices](#best-practices)

---

## React Native Setup

### Project Initialization

```bash
# Using React Native CLI
npx @react-native-community/cli init MyApp --template react-native-template-typescript

# Using Expo
npx create-expo-app MyApp --template blank-typescript

# Using Ignite (boilerplate)
npx ignite-cli new MyApp

# Navigate to project
cd MyApp

# Install dependencies
npm install
```

### Configuration

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "commonjs",
    "lib": ["es2017"],
    "jsx": "react-native",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "noEmit": true,
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["./components/*"],
      "@/screens/*": ["./screens/*"],
      "@/navigation/*": ["./navigation/*"],
      "@/services/*": ["./services/*"],
      "@/hooks/*": ["./hooks/*"],
      "@/utils/*": ["./utils/*"],
      "@/types/*": ["./types/*"],
      "@/constants/*": ["./constants/*"]
    }
  },
  "exclude": [
    "node_modules",
    "babel.config.js",
    "metro.config.js",
    "jest.config.js"
  ]
}

// babel.config.js
module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    'react-native-reanimated/plugin',
    [
      'module-resolver',
      {
        root: ['./src'],
        alias: {
          '@': './',
        '@/components': './components',
          '@/screens': './screens',
          '@/navigation': './navigation',
          '@/services': './services',
          '@/hooks': './hooks',
          '@/utils': './utils',
          '@/types': './types',
          '@/constants': './constants',
        },
      },
    ],
  ],
};

// metro.config.js
const { getDefaultConfig } = require('@expo/metro-config');

const config = getDefaultConfig(__dirname);

module.exports = {
  ...config,
  resolver: {
    sourceExts: ['jsx', 'js', 'ts', 'tsx', 'json'],
    assetExts: ['glb', 'gltf', 'png', 'jpg', 'jpeg', 'svg'],
  },
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
  },
};
```

---

## Project Structure

### Recommended Structure

```
src/
├── assets/              # Images, fonts, etc.
├── components/           # Reusable components
│   ├── common/          # Generic components
│   ├── buttons/         # Button variants
│   ├── inputs/          # Input components
│   └── cards/           # Card components
├── screens/             # Screen components
│   ├── auth/            # Authentication screens
│   ├── home/            # Home screen
│   ├── profile/         # Profile screen
│   └── settings/        # Settings screen
├── navigation/          # Navigation configuration
├── services/            # API and business logic
│   ├── api/             # API clients
│   ├── auth/            # Authentication service
│   └── storage/         # Local storage
├── hooks/               # Custom React hooks
├── utils/               # Utility functions
├── types/               # TypeScript types
├── constants/           # App constants
├── theme/               # Styling theme
│   ├── colors.ts
│   ├── typography.ts
│   └── spacing.ts
├── config/              # App configuration
├── store/               # State management
├── App.tsx              # Root component
└── index.ts             # Entry point
```

### Example Files

```typescript
// src/types/index.ts
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

export interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
}

export interface NavigationParams {
  userId?: string;
  productId?: string;
}

// src/constants/index.ts
export const API_URL = 'https://api.example.com';
export const APP_NAME = 'MyApp';
export const STORAGE_KEYS = {
  USER_TOKEN: '@user_token',
  USER_DATA: '@user_data',
};

// src/theme/colors.ts
export const Colors = {
  primary: '#007AFF',
  secondary: '#5856D6',
  success: '#34C759',
  warning: '#FF9500',
  danger: '#FF3B30',
  background: '#FFFFFF',
  surface: '#F2F2F7',
  text: '#000000',
  textSecondary: '#8E8E93',
  border: '#C6C6C8',
  transparent: 'rgba(0, 0, 0, 0)',
};

// src/theme/spacing.ts
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};
```

---

## Navigation

### React Navigation Setup

```typescript
// src/navigation/types.ts
export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
  Home: undefined;
  Profile: { userId: string };
  ProductDetails: { productId: string };
};

export type MainTabParamList = {
  Home: undefined;
  Search: undefined;
  Cart: undefined;
  Profile: undefined;
};

// src/navigation/AppNavigator.tsx
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import type { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: Colors.primary,
        headerShown: false,
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <HomeIcon color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Search"
        component={SearchScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <SearchIcon color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Cart"
        component={CartScreen}
        options={{
          tabBarBadge: 3,
          tabBarIcon: ({ color }) => (
            <CartIcon color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarIcon: ({ color }) => (
            <ProfileIcon color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
}

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}
      >
        <Stack.Screen name="Auth" component={AuthScreen} />
        <Stack.Screen name="Main" component={MainTabs} />
        <Stack.Screen
          name="Profile"
          component={ProfileScreen}
          options={{
            headerShown: true,
            headerTitle: 'Profile',
          }}
        />
        <Stack.Screen
          name="ProductDetails"
          component={ProductDetailsScreen}
          options={{
            headerShown: true,
            headerTitle: 'Product Details',
            presentation: 'card',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// src/navigation/hooks.ts
import type { RouteProp } from '@react-navigation/native';
import type { StackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from './types';

export type AppNavigationProp = StackNavigationProp<RootStackParamList>;
export type AppRouteProp = RouteProp<RootStackParamList>;

export const useNavigation = () => useNavigation<AppNavigationProp>();
export const useRoute = () => useRoute<AppRouteProp>();
```

### Navigation Hooks

```typescript
// src/hooks/useNavigation.ts
import { useNavigation as useReactNavigation } from '@react-navigation/native';
import type { RootStackParamList } from '@/navigation/types';

export function useNavigation() {
  const navigation = useReactNavigation<StackNavigationProp<RootStackParamList>>();

  const navigate = (screen: keyof RootStackParamList, params?: any) => {
    navigation.navigate(screen as any, params);
  };

  const goBack = () => {
    navigation.goBack();
  };

  const reset = (screen: keyof RootStackParamList) => {
    navigation.reset({
      index: 0,
      routes: [{ name: screen as any }],
    });
  };

  const push = (screen: keyof RootStackParamList, params?: any) => {
    navigation.push(screen as any, params);
  };

  return {
    navigate,
    goBack,
    reset,
    push,
  };
}

// Usage
function ProductCard({ product }: { product: Product }) {
  const { navigate } = useNavigation();

  const handlePress = () => {
    navigate('ProductDetails', { productId: product.id });
  };

  return (
    <TouchableOpacity onPress={handlePress}>
      <ProductCardUI product={product} />
    </TouchableOpacity>
  );
}
```

---

## State Management

### Context API Pattern

```typescript
// src/store/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { User } from '@/types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (user: User) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadAuthData();
  }, []);

  const loadAuthData = async () => {
    try {
      const [storedToken, storedUser] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.USER_TOKEN),
        AsyncStorage.getItem(STORAGE_KEYS.USER_DATA),
      ]);

      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      }
    } catch (error) {
      console.error('Error loading auth data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await authService.login(email, password);
      setToken(response.token);
      setUser(response.user);

      await Promise.all([
        AsyncStorage.setItem(STORAGE_KEYS.USER_TOKEN, response.token),
        AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(response.user)),
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await authService.logout();

      await Promise.all([
        AsyncStorage.removeItem(STORAGE_KEYS.USER_TOKEN),
        AsyncStorage.removeItem(STORAGE_KEYS.USER_DATA),
      ]);

      setToken(null);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const updateUser = (updatedUser: User) => {
    setUser(updatedUser);
    AsyncStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(updatedUser));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Custom Hooks

```typescript
// src/hooks/useFetch.ts
import { useState, useEffect, useCallback } from 'react';

export function useFetch<T>(
  url: string,
  options?: RequestInit
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url, options);
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [url, options]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
function ProductList() {
  const { data: products, loading, error, refetch } = useFetch<Product[]>(
    `${API_URL}/products`
  );

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <FlatList
      data={products}
      renderItem={({ item }) => <ProductCard product={item} />}
      keyExtractor={(item) => item.id}
      onRefresh={refetch}
      refreshing={loading}
    />
  );
}

// src/hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchInput() {
  const [searchText, setSearchText] = useState('');
  const debouncedSearch = useDebounce(searchText);

  useEffect(() => {
    // Perform search with debounced value
    performSearch(debouncedSearch);
  }, [debouncedSearch]);

  return (
    <TextInput
      value={searchText}
      onChangeText={setSearchText}
      placeholder="Search..."
    />
  );
}
```

---

## Styling Patterns

### Styled Components

```typescript
// src/components/common/Container.tsx
import styled from 'styled-components/native';

export const Container = styled.View`
  flex: 1;
  background-color: ${Colors.background};
  padding: ${Spacing.md}px;
`;

export const Card = styled.View`
  background-color: ${Colors.surface};
  border-radius: 12px;
  padding: ${Spacing.md}px;
  margin-bottom: ${Spacing.sm}px;
  shadow-color: rgba(0, 0, 0, 0.1);
  shadow-offset: 0px 2px;
  shadow-opacity: 1;
  shadow-radius: 4px;
  elevation: 2;
`;

export const Button = styled.TouchableOpacity<{ variant?: 'primary' | 'secondary' }>`
  background-color: ${props => props.variant === 'secondary' ? Colors.secondary : Colors.primary};
  padding: ${Spacing.md}px ${Spacing.lg}px;
  border-radius: 8px;
  align-items: center;
  justify-content: center;
  min-height: 48px;
`;

export const ButtonText = styled.Text<{ variant?: 'primary' | 'secondary' }>`
  color: ${Colors.background};
  font-size: 16px;
  font-weight: 600;
`;

export const Input = styled.TextInput`
  background-color: ${Colors.surface};
  border: 1px solid ${Colors.border};
  border-radius: 8px;
  padding: ${Spacing.md}px;
  font-size: 16px;
  color: ${Colors.text};
`;

// Usage
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    await authService.login(email, password);
  };

  return (
    <Container>
      <Card>
        <Input
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <Input
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        <Button variant="primary" onPress={handleLogin}>
          <ButtonText>Login</ButtonText>
        </Button>
      </Card>
    </Container>
  );
}
```

### Theme Provider

```typescript
// src/theme/ThemeProvider.tsx
import React, { createContext, useContext, useState } from 'react';
import { useColorScheme } from 'react-native';
import { Colors, DarkColors } from './colors';

interface Theme {
  colors: typeof Colors;
  isDark: boolean;
}

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const systemColorScheme = useColorScheme();
  const [isDark, setIsDark] = useState(systemColorScheme === 'dark');

  const theme: Theme = {
    colors: isDark ? DarkColors : Colors,
    isDark,
  };

  const toggleTheme = () => {
    setIsDark(!isDark);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// src/theme/colors.ts
export const Colors = {
  primary: '#007AFF',
  secondary: '#5856D6',
  background: '#FFFFFF',
  surface: '#F2F2F7',
  text: '#000000',
  textSecondary: '#8E8E93',
  border: '#C6C6C8',
  success: '#34C759',
  warning: '#FF9500',
  danger: '#FF3B30',
};

export const DarkColors = {
  ...Colors,
  background: '#000000',
  surface: '#1C1C1E',
  text: '#FFFFFF',
  textSecondary: '#98989D',
  border: '#38383A',
};
```

---

## Platform-Specific Code

### Platform Module

```typescript
// src/utils/platform.ts
import { Platform, PlatformIOS, PlatformAndroid } from 'react-native';

export const isIOS = Platform.OS === 'ios';
export const isAndroid = Platform.OS === 'android';

export const getPlatformSpecificValue = <T, U>(
  iosValue: T,
  androidValue: U
): T | U => {
  return Platform.select({
    ios: iosValue,
    android: androidValue,
  })!;
};

export const getSafeAreaPadding = () => {
  if (isIOS) {
    return {
      paddingTop: 44, // Status bar height on iOS
    };
  }

  return {
    paddingTop: 0,
  };
};

export const getStatusBarHeight = () => {
  return Platform.select({
    ios: 44,
    android: StatusBar.currentHeight || 24,
  })!;
};

// Usage
function PlatformAwareComponent() {
  const padding = getSafeAreaPadding();

  return (
    <View style={[styles.container, padding]}>
      <Text style={styles.text}>
        {getPlatformSpecificValue('iOS', 'Android')}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  text: {
    fontSize: 16,
  },
});
```

### Platform-Specific Components

```typescript
// src/components/platform/StatusBar.tsx
import { StatusBar, Platform, StatusBarStyle } from 'react-native';

interface StatusBarProps {
  barStyle?: StatusBarStyle;
  backgroundColor?: string;
}

export function CustomStatusBar({
  barStyle = 'dark-content',
  backgroundColor = '#FFFFFF',
}: StatusBarProps) {
  return (
    <>
      <StatusBar
        barStyle={barStyle}
        backgroundColor={backgroundColor}
        translucent={Platform.OS === 'android'}
      />
      {Platform.OS === 'android' && (
        <View style={{ height: StatusBar.currentHeight, backgroundColor }} />
      )}
    </>
  );
}

// src/components/platform/SafeArea.tsx
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export function SafeArea({ children }: { children: React.ReactNode }) {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={{
        paddingTop: insets.top,
        paddingBottom: insets.bottom,
        paddingLeft: insets.left,
        paddingRight: insets.right,
      }}
    >
      {children}
    </View>
  );
}
```

---

## Native Modules

### Creating Native Modules

```typescript
// ios/MyNativeModule.m
#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(MyNativeModule, NSObject, RCTBridgeModule)

@end

@implementation RCT_EXTERN_MODULE(MyNativeModule)

RCT_EXPORT_MODULE();

RCT_EXPORT_METHOD(getDeviceName:(RCTPromiseResolveBlock)resolve
                  reject:(RCTPromiseRejectBlock)reject) {
  NSString *deviceName = [[UIDevice currentDevice] name];
  resolve(deviceName);
}

@end

// android/app/src/main/java/com/mynativemodule/MyNativeModule.java
package com.mynativemodule;

import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.Promise;

public class MyNativeModule extends ReactContextBaseJavaModule {

  MyNativeModule(ReactApplicationContext reactContext) {
    super(reactContext);
  }

  @Override
  public String getName() {
    return "MyNativeModule";
  }

  @ReactMethod
  public void getDeviceName(Promise promise) {
    String deviceName = android.os.Build.MODEL;
    promise.resolve(deviceName);
  }
}

// src/modules/MyNativeModule.ts
import { NativeModules, NativeEventEmitter } from 'react-native';

interface MyNativeModuleType {
  getDeviceName(): Promise<string>;
}

const MyNativeModule = NativeModules.MyNativeModule as MyNativeModuleType;

export function useDeviceName() {
  const [deviceName, setDeviceName] = useState<string | null>(null);

  useEffect(() => {
    MyNativeModule.getDeviceName().then(setDeviceName);
  }, []);

  return deviceName;
}
```

---

## Performance Optimization

### Memoization

```typescript
import React, { memo, useMemo, useCallback } from 'react';

// Memoize expensive components
const ExpensiveComponent = memo(function ExpensiveComponent({
  data,
}: {
  data: any[];
}) {
  const processedData = useMemo(() => {
    return data.map(item => {
      // Expensive processing
      return { ...item, processed: true };
    });
  }, [data]);

  return (
    <FlatList
      data={processedData}
      renderItem={({ item }) => <Item item={item} />}
      keyExtractor={(item) => item.id}
    />
  );
});

// Memoize callback functions
function ParentComponent() {
  const [items, setItems] = useState([]);

  const handleItemPress = useCallback((itemId: string) => {
    console.log('Item pressed:', itemId);
  }, []);

  const renderItem = useCallback(({ item }: { item: any }) => (
    <Item item={item} onPress={handleItemPress} />
  ), [handleItemPress]);

  return (
    <FlatList
      data={items}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
    />
  );
}
```

### FlatList Optimization

```typescript
function OptimizedProductList({ products }: { products: Product[] }) {
  const renderItem = useCallback(({ item }: { item: Product }) => (
    <ProductCard product={item} />
  ), []);

  const keyExtractor = useCallback((item: Product) => item.id, []);

  const getItemLayout = useCallback((data, index) => ({
    length: 200, // Fixed height
    offset: 200 * index,
    index,
  }), []);

  return (
    <FlatList
      data={products}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      getItemLayout={getItemLayout}
      removeClippedSubviews={true}
      maxToRenderPerBatch={10}
      windowSize={10}
      initialNumToRender={10}
    />
  );
}
```

---

## Image Handling

### Image Optimization

```typescript
import { Image, ImageStyle } from 'react-native';
import FastImage from 'react-native-fast-image';

// Using FastImage for optimized loading
export function OptimizedImage({
  source,
  style,
}: {
  source: string;
  style?: ImageStyle;
}) {
  return (
    <FastImage
      source={{
        uri: source,
        priority: FastImage.priority.normal,
        cache: FastImage.cacheControl.immutable,
      }}
      style={style}
      resizeMode={FastImage.resizeMode.contain}
    />
  );
}

// Progressive image loading
export function ProgressiveImage({
  thumbnailSource,
  source,
  style,
}: {
  thumbnailSource: string;
  source: string;
  style?: ImageStyle;
}) {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <View style={style}>
      <Image
        source={{ uri: thumbnailSource }}
        style={[StyleSheet.absoluteFill, { opacity: isLoaded ? 0 : 1 }]}
      />
      <FastImage
        source={{ uri: source }}
        style={StyleSheet.absoluteFill}
        onLoad={() => setIsLoaded(true)}
      />
    </View>
  );
}
```

---

## Offline Support

### Offline Storage

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';
import { NetInfo } from '@react-native-community/netinfo';

export function useOfflineStorage<T>(key: string) {
  const [data, setData] = useState<T | null>(null);
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    loadData();
    setupNetInfo();
  }, []);

  const loadData = async () => {
    try {
      const stored = await AsyncStorage.getItem(key);
      if (stored) {
        setData(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const saveData = async (newData: T) => {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(newData));
      setData(newData);
    } catch (error) {
      console.error('Error saving data:', error);
    }
  };

  const setupNetInfo = () => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected!);
    });

    return unsubscribe;
  };

  return {
    data,
    isOnline,
    saveData,
    loadData,
  };
}

// Usage
function ProductList() {
  const { data: products, isOnline, saveData } = useOfflineStorage<Product[]>('products');

  useEffect(() => {
    if (isOnline) {
      fetchProducts().then(saveData);
    }
  }, [isOnline]);

  if (!isOnline && !products) {
    return <OfflineMessage />;
  }

  return (
    <FlatList
      data={products || []}
      renderItem={({ item }) => <ProductCard product={item} />}
      keyExtractor={(item) => item.id}
    />
  );
}
```

---

## Debugging

### Flipper Integration

```typescript
// metro.config.js
const { getDefaultConfig } = require('@expo/metro-config');

const config = getDefaultConfig(__dirname);

module.exports = {
  ...config,
  server: {
    enhanceMiddleware: (middleware) => {
      return (req, res, next) => {
        if (req.url.startsWith('/debugger-ui')) {
          return next();
        }
        return middleware(req, res, next);
      };
    },
  },
};

// App.tsx
if (__DEV__) {
  import { enableFlipper } from 'react-native-flipper';
  enableFlipper();
}
```

---

## Testing

### Component Testing

```typescript
// __tests__/components/Button.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Button, ButtonText } from '@/components/common/Container';

describe('Button', () => {
  it('renders correctly', () => {
    const { getByText } = render(
      <Button onPress={jest.fn()}>
        <ButtonText>Click me</ButtonText>
      </Button>
    );

    expect(getByText('Click me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <Button onPress={onPress}>
        <ButtonText>Click me</ButtonText>
      </Button>
    );

    fireEvent.press(getByText('Click me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

---

## Common Libraries

### Essential Libraries

```json
{
  "dependencies": {
    "@react-navigation/native": "^6.0.0",
    "@react-navigation/native-stack": "^6.0.0",
    "@react-navigation/bottom-tabs": "^6.0.0",
    "react-native-screens": "^3.0.0",
    "react-native-safe-area-context": "^4.0.0",
    "react-native-gesture-handler": "^2.0.0",
    "react-native-reanimated": "^3.0.0",
    "@react-native-async-storage/async-storage": "^1.0.0",
    "react-native-fast-image": "^8.0.0",
    "@react-native-community/netinfo": "^9.0.0",
    "styled-components": "^6.0.0",
    "@react-native-firebase/app": "^18.0.0",
    "@react-native-firebase/auth": "^18.0.0",
    "@react-native-firebase/firestore": "^18.0.0",
    "@react-native-firebase/messaging": "^18.0.0",
    "react-native-maps": "^1.0.0",
    "react-native-geolocation-service": "^5.0.0",
    "react-native-permissions": "^3.0.0",
    "react-native-linear-gradient": "^2.0.0",
    "react-native-svg": "^14.0.0",
    "react-native-vector-icons": "^10.0.0"
  },
  "devDependencies": {
    "@testing-library/react-native": "^12.0.0",
    "typescript": "^5.0.0",
    "@types/react": "^18.0.0",
    "@types/react-native": "^0.72.0"
  }
}
```

---

## Best Practices

### Performance Best Practices

```typescript
// 1. Use useCallback for functions passed to children
function Parent() {
  const [count, setCount] = useState(0);

  const handleIncrement = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return <Child onIncrement={handleIncrement} />;
}

// 2. Use useMemo for expensive calculations
function ExpensiveComponent({ items }: { items: any[] }) {
  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => a.id - b.id);
  }, [items]);

  return <List items={sortedItems} />;
}

// 3. Use keyExtractor for FlatList
function List({ items }: { items: any[] }) {
  return (
    <FlatList
      data={items}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <Item item={item} />}
    />
  );
}

// 4. Avoid inline functions in render
function BadExample({ items }: { items: any[] }) {
  return (
    <FlatList
      data={items}
      renderItem={({ item }) => (
        <Item onPress={() => console.log(item.id)} /> // Bad: Creates new function each render
      )}
    />
  );
}

function GoodExample({ items }: { items: any[] }) {
  const handlePress = useCallback((id: string) => {
    console.log(id);
  }, []);

  return (
    <FlatList
      data={items}
      renderItem={({ item }) => (
        <Item onPress={() => handlePress(item.id)} /> // Good: Uses callback
      )}
    />
  );
}

// 5. Use StyleSheet.create for static styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  text: {
    fontSize: 16,
  },
});

function Component() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Hello</Text>
    </View>
  );
}
```

---

---

## Quick Start

### Create React Native App

```bash
# Using Expo
npx create-expo-app MyApp
cd MyApp
npm start

# Using React Native CLI
npx react-native init MyApp
cd MyApp
npm run android  # or ios
```

### Basic App Structure

```typescript
// App.tsx
import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createStackNavigator } from '@react-navigation/stack'

const Stack = createStackNavigator()

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}
```

---

## Production Checklist

- [ ] **Project Structure**: Organized folder structure
- [ ] **Navigation**: Navigation library configured (React Navigation)
- [ ] **State Management**: State management solution (Redux, Zustand)
- [ ] **Styling**: Consistent styling approach (StyleSheet, styled-components)
- [ ] **Platform-Specific**: Platform-specific code handled
- [ ] **Performance**: Performance optimizations (memoization, FlatList)
- [ ] **Testing**: Unit and integration tests
- [ ] **Error Handling**: Error boundaries and error handling
- [ ] **Offline Support**: Offline functionality if needed
- [ ] **Push Notifications**: Push notification setup
- [ ] **App Store**: App store deployment configured
- [ ] **Analytics**: Analytics integration

---

## Anti-patterns

### ❌ Don't: Inline Styles Everywhere

```tsx
// ❌ Bad - Inline styles
<View style={{ padding: 10, margin: 5, backgroundColor: '#fff' }}>
```

```tsx
// ✅ Good - StyleSheet
const styles = StyleSheet.create({
  container: {
    padding: 10,
    margin: 5,
    backgroundColor: '#fff'
  }
})

<View style={styles.container}>
```

### ❌ Don't: No Error Boundaries

```tsx
// ❌ Bad - No error handling
function App() {
  return <ComponentThatMightCrash />
}
```

```tsx
// ✅ Good - Error boundary
class ErrorBoundary extends React.Component {
  // Error boundary implementation
}

function App() {
  return (
    <ErrorBoundary>
      <ComponentThatMightCrash />
    </ErrorBoundary>
  )
}
```

---

## Integration Points

- **State Management** (`02-frontend/state-management/`) - State patterns
- **Mobile CI/CD** (`31-mobile-development/mobile-ci-cd/`) - Deployment
- **Push Notifications** (`31-mobile-development/push-notifications/`) - Notifications

---

## Further Reading

- [React Native Documentation](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Community](https://reactnative.directory/)
