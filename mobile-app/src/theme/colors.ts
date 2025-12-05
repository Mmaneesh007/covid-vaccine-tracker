export const colors = {
    background: '#0F172A', // Dark Slate Blue (Background)
    surface: '#1E293B',    // Lighter Slate (Cards)
    primary: '#3B82F6',    // Bright Blue (Action)
    secondary: '#10B981',  // Emerald Green (Success/Safe)
    danger: '#EF4444',     // Red (High Risk)
    warning: '#F59E0B',    // Amber (Medium Risk)
    text: '#F8FAFC',       // Off-white text
    textSecondary: '#94A3B8', // Grey text
    border: '#334155',     // Border

    // Gradients candidates
    gradientStart: '#1E293B',
    gradientEnd: '#0F172A',
};

export const spacing = {
    s: 8,
    m: 16,
    l: 24,
    xl: 32,
};

export const typography = {
    header: {
        fontSize: 24,
        fontWeight: '700',
        color: colors.text,
    },
    subHeader: {
        fontSize: 18,
        fontWeight: '600',
        color: colors.text,
    },
    body: {
        fontSize: 16,
        color: colors.textSecondary,
    },
};
