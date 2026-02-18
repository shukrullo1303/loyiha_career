import React, { useEffect } from 'react'
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native'
import { useQuery } from 'react-query'
import { useAuthStore } from '../store/authStore'
import apiClient from '../api/apiClient'

export default function DashboardScreen() {
  const { token, user } = useAuthStore()

  const { data: locations } = useQuery(
    'locations',
    async () => {
      const response = await apiClient.get(`/locations/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      return response.data
    },
    { enabled: !!token }
  )

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Дашборд</Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Локациялар</Text>
        <Text style={styles.cardValue}>{locations?.length || 0}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Ходимлар</Text>
        <Text style={styles.cardValue}>0</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Рискли локациялар</Text>
        <Text style={styles.cardValue}>0</Text>
      </View>
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 10,
  },
  cardValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1976d2',
  },
})
