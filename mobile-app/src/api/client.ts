import axios from 'axios';

// Public Tunnel URL for global access
const BASE_URL = 'https://33025155877bc0.lhr.life/api/v1';

export const apiClient = axios.create({
    baseURL: BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'sk_live_e7d7160fe461379b6e42050c99e62dec', // Using valid development key
    },
});

export const getVaccinationStats = async (country: string = 'World') => {
    try {
        // Endpoint: /api/v1/countries/{country}
        const response = await apiClient.get(`/countries/${country}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching stats:', error);
        throw error;
    }
};

export const getCountryList = async () => {
    try {
        // Endpoint: /api/v1/countries
        const response = await apiClient.get('/countries');
        return response.data;
    } catch (error) {
        console.error('Error fetching countries:', error);
        throw error;
    }
};

export const getCountryTimeseries = async (country: string, metric: string = 'total_vaccinations', limit: number = 7) => {
    try {
        // Endpoint: /api/v1/countries/{country}/timeseries
        const response = await apiClient.get(`/countries/${country}/timeseries`, {
            params: { metric, limit }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching timeseries:', error);
        throw error;
    }
};
