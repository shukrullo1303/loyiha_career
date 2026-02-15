import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { StatusBar } from 'expo-status-bar'
import { Ionicons } from '@expo/vector-icons'

import LoginScreen from './src/screens/LoginScreen'
import DashboardScreen from './src/screens/DashboardScreen'
import LocationsScreen from './src/screens/LocationsScreen'
import AnalyticsScreen from './src/screens/AnalyticsScreen'
import { useAuthStore } from './src/store/authStore'

const Stack = createNativeStackNavigator()
const Tab = createBottomTabNavigator()

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: any

          if (route.name === 'Dashboard') {
            iconName = focused ? 'home' : 'home-outline'
          } else if (route.name === 'Locations') {
            iconName = focused ? 'location' : 'location-outline'
          } else if (route.name === 'Analytics') {
            iconName = focused ? 'analytics' : 'analytics-outline'
          }

          return <Ionicons name={iconName} size={size} color={color} />
        },
        tabBarActiveTintColor: '#1976d2',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} options={{ title: 'Дашборд' }} />
      <Tab.Screen name="Locations" component={LocationsScreen} options={{ title: 'Локациялар' }} />
      <Tab.Screen name="Analytics" component={AnalyticsScreen} options={{ title: 'Аналитика' }} />
    </Tab.Navigator>
  )
}

export default function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          <Stack.Screen name="Login" component={LoginScreen} />
        ) : (
          <Stack.Screen name="Main" component={MainTabs} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  )
}
