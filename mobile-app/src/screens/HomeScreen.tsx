import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, TextInput, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, spacing, typography } from '../theme/colors';
import { getCountryList } from '../api/client';
import { StatusBar } from 'expo-status-bar';

const HomeScreen = () => {
    const navigation = useNavigation<any>();
    const [countries, setCountries] = useState<string[]>([]);
    const [filteredCountries, setFilteredCountries] = useState<string[]>([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadCountries();
    }, []);

    const loadCountries = async () => {
        try {
            const data = await getCountryList();
            if (data && data.countries) {
                setCountries(data.countries);
                setFilteredCountries(data.countries);
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (text: string) => {
        setSearch(text);
        if (text) {
            const filtered = countries.filter(c =>
                c.toLowerCase().includes(text.toLowerCase())
            );
            setFilteredCountries(filtered);
        } else {
            setFilteredCountries(countries);
        }
    };

    const renderItem = ({ item }: { item: string }) => (
        <TouchableOpacity
            style={styles.card}
            onPress={() => navigation.navigate('Detail', { country: item })}
        >
            <View style={styles.cardIcon}>
                <Text style={styles.cardIconText}>{item.charAt(0)}</Text>
            </View>
            <Text style={styles.countryName}>{item}</Text>
            <Text style={styles.arrow}>›</Text>
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Vaccine Tracker</Text>
                <Text style={styles.subtitle}>Safe Mode: No Detail Screen</Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background,
    },
    center: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    header: {
        padding: spacing.m,
        paddingBottom: spacing.s,
    },
    title: {
        ...typography.header,
        fontSize: 32,
    },
    subtitle: {
        ...typography.body,
        marginTop: 4,
    },
    searchContainer: {
        padding: spacing.m,
        paddingTop: 0,
    },
    searchInput: {
        backgroundColor: colors.surface,
        borderRadius: 12,
        padding: spacing.m,
        color: colors.text,
        fontSize: 16,
        borderWidth: 1,
        borderColor: colors.border,
    },
    list: {
        padding: spacing.m,
    },
    card: {
        backgroundColor: colors.surface,
        flexDirection: 'row',
        alignItems: 'center',
        padding: spacing.m,
        marginBottom: spacing.s,
        borderRadius: 12,
    },
    cardIcon: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: colors.primary,
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: spacing.m,
    },
    cardIconText: {
        color: '#FFF',
        fontWeight: 'bold',
        fontSize: 18,
    },
    countryName: {
        ...typography.subHeader,
        flex: 1,
        fontSize: 16,
    },
    arrow: {
        color: colors.textSecondary,
        fontSize: 24,
        fontWeight: '300',
    },
});

export default HomeScreen;
