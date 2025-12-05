import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Dimensions, ScrollView, ActivityIndicator } from 'react-native';
import { RouteProp, useRoute, useNavigation } from '@react-navigation/native';
import { LineChart } from 'react-native-chart-kit';
import { colors, spacing, typography } from '../theme/colors';
import { getVaccinationStats, getCountryTimeseries } from '../api/client';
import { SafeAreaView } from 'react-native-safe-area-context';

type RootStackParamList = {
    Detail: { country: string };
};

type DetailScreenRouteProp = RouteProp<RootStackParamList, 'Detail'>;

const DetailScreen = () => {
    const route = useRoute<DetailScreenRouteProp>();
    const navigation = useNavigation();
    const { country } = route.params;

    const [stats, setStats] = useState<any>(null);
    const [chartData, setChartData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, [country]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [statsData, timeseries] = await Promise.all([
                getVaccinationStats(country),
                getCountryTimeseries(country, 'total_vaccinations', 7) // Last 7 days
            ]);

            setStats(statsData);

            if (timeseries && timeseries.data) {
                const labels = timeseries.data.map((d: any) => d.date.slice(5)); // 'MM-DD'
                const values = timeseries.data.map((d: any) => d.value / 1000000); // In Millions

                setChartData({
                    labels,
                    datasets: [{ data: values }]
                });
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color={colors.primary} />
            </View>
        );
    }

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView>
                <View style={styles.header}>
                    <Text style={styles.countryName}>{country}</Text>
                    <Text style={styles.date}>Data as of {stats?.date}</Text>
                </View>

                {/* Main Stats Cards */}
                <View style={styles.statsContainer}>
                    <StatCard label="Total Doses" value={stats?.total_vaccinations?.toLocaleString()} color={colors.primary} />
                    <StatCard label="Fully Vaccinated" value={stats?.people_fully_vaccinated?.toLocaleString()} color={colors.secondary} />
                    <StatCard label="Coverage" value={`${stats?.people_fully_vaccinated_per_hundred}%`} color={colors.warning} />
                </View>

                {/* Chart */}
                {chartData && (
                    <View style={styles.chartContainer}>
                        <Text style={styles.chartTitle}>Vaccination Trend (Millions)</Text>
                        <LineChart
                            data={chartData}
                            width={Dimensions.get('window').width - 32}
                            height={220}
                            chartConfig={{
                                backgroundColor: colors.surface,
                                backgroundGradientFrom: colors.surface,
                                backgroundGradientTo: colors.surface,
                                decimalPlaces: 1,
                                color: (opacity = 1) => `rgba(59, 130, 246, ${opacity})`,
                                labelColor: (opacity = 1) => colors.textSecondary,
                                style: { borderRadius: 16 },
                                propsForDots: { r: 4, strokeWidth: 2, stroke: colors.primary }
                            }}
                            bezier
                            style={styles.chart}
                        />
                    </View>
                )}
            </ScrollView>
        </SafeAreaView>
    );
};

const StatCard = ({ label, value, color }: { label: string, value: string, color: string }) => (
    <View style={[styles.card, { borderLeftColor: color }]}>
        <Text style={styles.cardLabel}>{label}</Text>
        <Text style={[styles.cardValue, { color }]}>{value || 'N/A'}</Text>
    </View>
);

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background,
    },
    loadingContainer: {
        flex: 1,
        backgroundColor: colors.background,
        justifyContent: 'center',
        alignItems: 'center',
    },
    header: {
        padding: spacing.m,
        marginBottom: spacing.s,
    },
    countryName: {
        ...typography.header,
        fontSize: 32,
    },
    date: {
        ...typography.body,
        marginTop: 4,
    },
    statsContainer: {
        padding: spacing.m,
    },
    card: {
        backgroundColor: colors.surface,
        padding: spacing.m,
        borderRadius: 12,
        marginBottom: spacing.m,
        borderLeftWidth: 4,
    },
    cardLabel: {
        ...typography.body,
        fontSize: 14,
        marginBottom: 4,
    },
    cardValue: {
        fontSize: 24,
        fontWeight: '700',
    },
    chartContainer: {
        margin: spacing.m,
        padding: spacing.m,
        backgroundColor: colors.surface,
        borderRadius: 16,
        alignItems: 'center',
    },
    chartTitle: {
        ...typography.subHeader,
        marginBottom: spacing.m,
        alignSelf: 'flex-start',
    },
    chart: {
        marginVertical: 8,
        borderRadius: 16,
    },
});

export default DetailScreen;
