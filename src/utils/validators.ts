export const isValidEmail = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());

export const isValidIndianPhone = (value: string) => /^\d{10}$/.test(value.trim());

export const isValidName = (value: string) => /^[A-Za-z][A-Za-z .'-]{1,79}$/.test(value.trim());

export const isValidNumber = (value: string) => /^\d+(\.\d+)?$/.test(value.trim());

export const isValidYear = (value: string) => /^(19|20)\d{2}$/.test(value.trim());
