import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const cryptoExchangesHeaders = {
    'X-RapidAPI-Key': 'f0c0be62f0msh80fdcd9f4fd809ep157e82jsn5cf5657bd7a2',
    'X-RapidAPI-Host': 'coinranking1.p.rapidapi.com'
};

const baseUrl='https://coinranking1.p.rapidapi.com';

const createRequest = (url) => ({ url, headers: cryptoExchangesHeaders });

export const cryptoExchangesApi = createApi({
    reducerPath: 'cryptoExchangesAPI',
    baseQuery: fetchBaseQuery({ baseUrl}),
    endpoints: (builder) =>({
        getExchanges: builder.query({
            query: (coinId) => createRequest(`/coin/${coinId}/exchanges`),
          }),
      
    })
})

export const {
     useGetExchangesQuery,
}=cryptoExchangesApi;