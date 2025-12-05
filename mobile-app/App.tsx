import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, ActivityIndicator, SafeAreaView, StatusBar, Platform, TextInput } from 'react-native';
import { getVaccinationStats } from './src/api/client';

// Simple types for stats
interface Stats {
  location: string;
  total_vaccinations: number;
  people_vaccinated: number;
  people_fully_vaccinated: number;
  date: string;
}

export default function App() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchStats = async (country: string = 'World') => {
    setLoading(true);
    setError(null);
    try {
      const target = country.trim() || 'World';
      const data = await getVaccinationStats(target);
      setStats(data);
    } catch (err) {
      setError(`Could not find data for "${country}". Check spelling or backend connection.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      fetchStats(searchQuery);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000000) {
      return (num / 1000000000).toFixed(2) + ' B';
    }
    if (num >= 1000000) {
      return (num / 1000000).toFixed(2) + ' M';
    }
    return num.toLocaleString();
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">

        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>💉 Vaccine Tracker</Text>
          <Text style={styles.headerSubtitle}>Real-time Global Data</Text>
        </View>

        {/* Search Bar */}
        <View style={styles.searchContainer}>
          <TextInput
            style={styles.searchInput}
            placeholder="Search country (e.g., India, USA)..."
            value={searchQuery}
            onChangeText={setSearchQuery}
            onSubmitEditing={handleSearch}
            returnKeyType="search"
          />
          <TouchableOpacity style={styles.searchButton} onPress={handleSearch}>
            <Text style={styles.searchButtonText}>🔍</Text>
          </TouchableOpacity>
        </View>

        {/* Content */}
        <View style={styles.content}>
          {loading ? (
            <View style={styles.centerContainer}>
              <ActivityIndicator size="large" color="#667eea" />
              <Text style={styles.loadingText}>Fetching latest data...</Text>
            </View>
          ) : error ? (
            <View style={styles.centerContainer}>
              <Text style={styles.errorText}>⚠️ {error}</Text>
              <TouchableOpacity style={styles.retryButton} onPress={() => fetchStats(searchQuery)}>
                <Text style={styles.retryButtonText}>Retry Connection</Text>
              </TouchableOpacity>
            </View>
          ) : stats ? (
            <>
              {/* Main Card */}
              <View style={styles.card}>
                <Text style={styles.locationTag}>🌍 {stats.location}</Text>

                <View style={styles.statRow}>
                  <Text style={styles.statLabel}>Total Doses</Text>
                  <Text style={styles.statValue}>{formatNumber(stats.total_vaccinations)}</Text>
                </View>

                <View style={styles.divider} />

                <View style={styles.statGrid}>
                  <View style={styles.statItem}>
                    <Text style={styles.subStatLabel}>Vaccinated</Text>
                    <Text style={styles.subStatValue}>{formatNumber(stats.people_vaccinated)}</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Text style={styles.subStatLabel}>Fully Vaxxed</Text>
                    <Text style={styles.subStatValue}>{formatNumber(stats.people_fully_vaccinated)}</Text>
                  </View>
                </View>

                <Text style={styles.dateText}>Updated: {stats.date}</Text>
              </View>

              {/* Action Button */}
              <TouchableOpacity style={styles.refreshButton} onPress={() => fetchStats(searchQuery || 'World')}>
                <Text style={styles.refreshButtonText}>🔄 Refresh Data</Text>
              </TouchableOpacity>

              <View style={styles.infoBox}>
                <Text style={styles.infoText}>
                  Run backend with: py app/api/main.py
                  Mobile checks: http://192.168.0.134:8001
                </Text>
              </View>
            </>
          ) : null}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f6f9fc',
    paddingTop: Platform.OS === 'android' ? 25 : 0,
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    marginBottom: 24,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: '#1a1a1a',
    letterSpacing: -0.5,
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#5f6368',
    marginTop: 4,
  },
  searchContainer: {
    flexDirection: 'row',
    marginBottom: 20,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  searchInput: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 16,
    fontSize: 16,
    color: '#2d3748',
  },
  searchButton: {
    backgroundColor: '#667eea',
    borderRadius: 10,
    padding: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchButtonText: {
    fontSize: 18,
  },
  content: {
    flex: 1,
  },
  centerContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  loadingText: {
    marginTop: 12,
    color: '#667eea',
    fontWeight: '500',
  },
  errorText: {
    color: '#e53e3e',
    textAlign: 'center',
    marginBottom: 16,
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 24,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 8,
    marginBottom: 20,
  },
  locationTag: {
    fontSize: 14,
    fontWeight: '700',
    color: '#667eea',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 20,
  },
  statRow: {
    marginBottom: 20,
  },
  statLabel: {
    fontSize: 16,
    color: '#718096',
    fontWeight: '600',
    marginBottom: 4,
  },
  statValue: {
    fontSize: 42,
    fontWeight: '800',
    color: '#2d3748',
    letterSpacing: -1,
  },
  divider: {
    height: 1,
    backgroundColor: '#e2e8f0',
    marginVertical: 20,
  },
  statGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statItem: {
    flex: 1,
  },
  subStatLabel: {
    fontSize: 14,
    color: '#718096',
    marginBottom: 4,
  },
  subStatValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#4a5568',
  },
  dateText: {
    marginTop: 20,
    fontSize: 12,
    color: '#a0aec0',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  retryButton: {
    backgroundColor: '#667eea',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 12,
  },
  retryButtonText: {
    color: 'white',
    fontWeight: '600',
  },
  refreshButton: {
    backgroundColor: '#2d3748',
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  refreshButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  infoBox: {
    marginTop: 30,
    padding: 15,
    backgroundColor: '#edf2f7',
    borderRadius: 12,
  },
  infoText: {
    fontSize: 12,
    color: '#718096',
    textAlign: 'center',
    fontFamily: 'monospace',
  }
});
