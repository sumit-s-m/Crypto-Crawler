import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const cryptoApiHeaders = {
    'X-RapidAPI-Key': 'f0c0be62f0msh80fdcd9f4fd809ep157e82jsn5cf5657bd7a2',
    'X-RapidAPI-Host': 'coinranking1.p.rapidapi.com'
};

const baseUrl='https://coinranking1.p.rapidapi.com';

const createRequest = (url) => ({ url, headers: cryptoApiHeaders });

export const cryptoApi = createApi({
    reducerPath: 'cryptoAPI',
    baseQuery: fetchBaseQuery({ baseUrl}),
    endpoints: (builder) => ({
      getCryptos: builder.query({
        query: (count) => createRequest(`/coins?limit=${count}`),
      }),
      getCryptoDetails: builder.query({
        query: (coinId) => createRequest(`/coin/${coinId}`),
      }),
      getCryptoHistory: builder.query({
        query: ({ coinId, timeperiod }) => createRequest(`coin/${coinId}/history?timeperiod=${timeperiod}`),
      }),
    }),
})

export const {
    useGetCryptosQuery,
    useGetCryptoDetailsQuery,
    // useGetExchangesQuery,
    useGetCryptoHistoryQuery,
  } = cryptoApi;