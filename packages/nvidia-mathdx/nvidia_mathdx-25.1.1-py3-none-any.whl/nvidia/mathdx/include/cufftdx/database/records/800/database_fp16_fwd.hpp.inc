//Copyright (c) 2019-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
//NVIDIA CORPORATION and its licensors retain all intellectual property
//and proprietary rights in and to this software, related documentation
//and any modifications thereto.  Any use, reproduction, disclosure or
//distribution of this software and related documentation without an express
//license agreement from NVIDIA CORPORATION is strictly prohibited.
//


template<> struct block_fft_record<33, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<33,   33,    1,    64,     0,  1948>
    >;
};

template<> struct block_fft_record<34, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    1,    64,     0,  1949>
    >;
};

template<> struct block_fft_record<35, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<35,   35,    1,    64,     0,  1950>
    >;
};

template<> struct block_fft_record<37, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<37,   37,    1,    64,     0,  1951>
    >;
};

template<> struct block_fft_record<38, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    1,    64,     0,  1952>
    >;
};

template<> struct block_fft_record<39, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<39,   39,    1,    64,     0,  1953>
    >;
};

template<> struct block_fft_record<40, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    2,    64,   160,  1955>,
        block_fft_implementation<20,   20,    2,    64,    80,  1954>,
        block_fft_implementation<10,   10,    4,    64,   160,  1956>,
        block_fft_implementation<40,   40,    1,    32,     0,  1957>
    >;
};

template<> struct block_fft_record<41, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<41,   41,    1,    64,     0,  1958>
    >;
};

template<> struct block_fft_record<42, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    1,    64,     0,  1959>
    >;
};

template<> struct block_fft_record<43, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<43,   43,    1,    64,     0,  1960>
    >;
};

template<> struct block_fft_record<44, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    1,    64,     0,  1961>
    >;
};

template<> struct block_fft_record<45, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<45,   45,    1,    64,     0,  1962>
    >;
};

template<> struct block_fft_record<46, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    1,    64,     0,  1963>
    >;
};

template<> struct block_fft_record<47, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<47,   47,    1,    64,     0,  1964>
    >;
};

template<> struct block_fft_record<48, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<48,   48,    1,    64,     0,  1965>
    >;
};

template<> struct block_fft_record<50, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<50,   50,    1,    64,     0,  1966>
    >;
};

template<> struct block_fft_record<51, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<51,   51,    1,    64,     0,  1967>
    >;
};

template<> struct block_fft_record<52, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    1,    64,     0,  1968>
    >;
};

template<> struct block_fft_record<53, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<53,   53,    1,    64,     0,  1969>
    >;
};

template<> struct block_fft_record<54, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<54,   54,    1,    64,     0,  1970>
    >;
};

template<> struct block_fft_record<55, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<55,   55,    1,    64,     0,  1971>
    >;
};

template<> struct block_fft_record<56, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    1,    64,     0,  1972>
    >;
};

template<> struct block_fft_record<57, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<57,   57,    1,    64,     0,  1973>
    >;
};

template<> struct block_fft_record<58, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    1,    64,     0,  1974>
    >;
};

template<> struct block_fft_record<59, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<59,   59,    1,    64,     0,  1975>
    >;
};

template<> struct block_fft_record<60, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    1,    64,     0,  1976>
    >;
};

template<> struct block_fft_record<61, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<61,   61,    1,    64,     0,  1977>
    >;
};

template<> struct block_fft_record<62, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    1,    64,     0,  1978>
    >;
};

template<> struct block_fft_record<63, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<63,   63,    1,    64,     0,  1979>
    >;
};

template<> struct block_fft_record<2, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 2,    2,    1,   256,     0,  1980>
    >;
};

template<> struct block_fft_record<4, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4,    1,   128,     0,  1981>,
        block_fft_implementation< 2,    2,    2,   256,     8,  1982>,
        block_fft_implementation< 2,    2,    2,   256,    16,  1983>
    >;
};

template<> struct block_fft_record<8, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    1,    64,     0,  1984>,
        block_fft_implementation< 4,    4,    2,   224,    16,  1985>,
        block_fft_implementation< 4,    4,    2,   256,    32,  1986>,
        block_fft_implementation< 2,    2,    4,   192,    16,  1987>,
        block_fft_implementation< 2,    2,    4,   256,    32,  1988>
    >;
};

template<> struct block_fft_record<16, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    1,    64,     0,  1989>,
        block_fft_implementation< 4,    4,    4,   128,    32,  1990>,
        block_fft_implementation< 4,    4,    4,   160,    64,  1991>,
        block_fft_implementation< 8,    8,    2,   192,    32,  1992>,
        block_fft_implementation< 8,    8,    2,   192,    64,  1993>,
        block_fft_implementation< 2,    2,    8,   128,    32,  1994>,
        block_fft_implementation< 2,    2,    8,   160,    64,  1995>
    >;
};

template<> struct block_fft_record<32, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,    1,    64,     0,  1996>,
        block_fft_implementation< 8,    8,    4,    60,   128,  1997>,
        block_fft_implementation< 8,    8,    4,    96,    64,  1998>,
        block_fft_implementation< 4,    4,    8,    64,   128,  1999>,
        block_fft_implementation< 4,    4,    8,   128,    64,  2000>,
        block_fft_implementation< 2,    2,   16,    60,   128,  2001>,
        block_fft_implementation<16,   16,    2,   192,   128,  2002>,
        block_fft_implementation< 2,    2,   16,    48,    64,  2003>,
        block_fft_implementation<16,   16,    2,    54,    64,  2004>
    >;
};

template<> struct block_fft_record<64, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    8,    32,   256,  2005>,
        block_fft_implementation< 8,    8,    8,    32,   128,  2006>,
        block_fft_implementation< 4,    4,   16,    24,   256,  2007>,
        block_fft_implementation< 4,    4,   16,    32,   128,  2008>,
        block_fft_implementation<16,   16,    4,    62,   256,  2009>,
        block_fft_implementation<16,   16,    4,    28,   128,  2010>,
        block_fft_implementation<32,   32,    2,    56,   256,  2011>,
        block_fft_implementation< 2,    2,   32,    24,   256,  2012>,
        block_fft_implementation< 2,    2,   32,    24,   128,  2013>,
        block_fft_implementation<32,   32,    2,    60,   128,  2014>,
        block_fft_implementation<64,   64,    1,    64,     0,  2015>
    >;
};

template<> struct block_fft_record<128, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    8,    16,   256,  2016>,
        block_fft_implementation< 8,    8,   16,    16,   512,  2017>,
        block_fft_implementation<16,   16,    8,    32,   512,  2018>,
        block_fft_implementation< 8,    8,   16,    16,   256,  2019>,
        block_fft_implementation< 4,    4,   32,     8,   512,  2020>,
        block_fft_implementation< 4,    4,   32,    16,   256,  2021>,
        block_fft_implementation<32,   32,    4,    30,   512,  2022>,
        block_fft_implementation<32,   32,    4,    32,   256,  2023>,
        block_fft_implementation< 2,    2,   64,    10,   512,  2024>,
        block_fft_implementation< 2,    2,   64,    10,   256,  2025>
    >;
};

template<> struct block_fft_record<256, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,   16,     8,   512,  2026>,
        block_fft_implementation< 8,    8,   32,     4,  1024,  2027>,
        block_fft_implementation< 8,    8,   32,     8,   512,  2028>,
        block_fft_implementation<16,   16,   16,     8,  1024,  2029>,
        block_fft_implementation<32,   32,    8,    16,  1024,  2030>,
        block_fft_implementation< 4,    4,   64,     4,  1024,  2031>,
        block_fft_implementation< 4,    4,   64,     8,   512,  2032>,
        block_fft_implementation<32,   32,    8,    16,   512,  2033>,
        block_fft_implementation< 2,    2,  128,     6,  1024,  2034>,
        block_fft_implementation< 2,    2,  128,     6,   512,  2035>
    >;
};

template<> struct block_fft_record<512, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,   64,     2,  2048,  2036>,
        block_fft_implementation< 8,    8,   64,     2,  1024,  2037>,
        block_fft_implementation<32,   32,   16,     4,  2048,  2039>,
        block_fft_implementation<16,   16,   32,     4,  1024,  2038>,
        block_fft_implementation<16,   16,   32,     4,  2048,  2041>,
        block_fft_implementation<32,   32,   16,     8,  1024,  2040>,
        block_fft_implementation< 4,    4,  128,     2,  2048,  2042>,
        block_fft_implementation< 4,    4,  128,     4,  1024,  2043>,
        block_fft_implementation< 2,    2,  256,     4,  2048,  2044>,
        block_fft_implementation< 2,    2,  256,     2,  1024,  2045>
    >;
};

template<> struct block_fft_record<1024, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,   32,     2,  4096,  2048>,
        block_fft_implementation<16,   16,   64,     2,  2048,  2046>,
        block_fft_implementation< 8,    8,  128,     2,  2048,  2049>,
        block_fft_implementation<32,   32,   32,     4,  2048,  2050>,
        block_fft_implementation< 8,    8,  128,     2,  4096,  2047>,
        block_fft_implementation<16,   16,   64,     2,  4096,  2051>,
        block_fft_implementation< 4,    4,  256,     2,  4096,  2052>,
        block_fft_implementation< 4,    4,  256,     2,  2048,  2053>,
        block_fft_implementation< 2,    2,  512,     2,  4096,  2054>,
        block_fft_implementation< 2,    2,  512,     2,  2048,  2055>
    >;
};

template<> struct block_fft_record<2048, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  128,     2,  4096,  2056>,
        block_fft_implementation< 8,    8,  256,     2,  4096,  2058>,
        block_fft_implementation< 8,    8,  256,     2,  8192,  2057>,
        block_fft_implementation<16,   16,  128,     2,  8192,  2059>,
        block_fft_implementation<32,   32,   64,     2,  8192,  2060>,
        block_fft_implementation<32,   32,   64,     2,  4096,  2061>,
        block_fft_implementation< 4,    4,  512,     2,  8192,  2062>,
        block_fft_implementation< 4,    4,  512,     2,  4096,  2063>,
        block_fft_implementation< 2,    2, 1024,     2,  8192,  2064>,
        block_fft_implementation< 2,    2, 1024,     2,  4096,  2065>
    >;
};

template<> struct block_fft_record<4096, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  256,     2,  8192,  2066>,
        block_fft_implementation< 8,    8,  512,     2,  8192,  2068>,
        block_fft_implementation<16,   16,  256,     2, 16384,  2069>,
        block_fft_implementation<32,   32,  128,     2, 16384,  2070>,
        block_fft_implementation< 8,    8,  512,     2, 16384,  2067>,
        block_fft_implementation<32,   32,  128,     2,  8192,  2071>,
        block_fft_implementation< 4,    4, 1024,     2, 16384,  2072>,
        block_fft_implementation< 4,    4, 1024,     2,  8192,  2073>
    >;
};

template<> struct block_fft_record<8192, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,  256,     2, 32768,  2075>,
        block_fft_implementation<32,   32,  256,     2, 16384,  2076>,
        block_fft_implementation<16,   16,  512,     2, 16384,  2074>,
        block_fft_implementation<16,   16,  512,     2, 32768,  2078>,
        block_fft_implementation< 8,    8, 1024,     2, 16384,  2079>,
        block_fft_implementation< 8,    8, 1024,     2, 32768,  2077>
    >;
};

template<> struct block_fft_record<16384, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,  512,     2, 65536,  3032>,
        block_fft_implementation<16,   16, 1024,     2, 32768,  2080>,
        block_fft_implementation<16,   16, 1024,     2, 65536,  3033>,
        block_fft_implementation<32,   32,  512,     2, 32768,  2081>
    >;
};

template<> struct block_fft_record<32768, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32, 1024,     2, 65536,  3034>
    >;
};

template<> struct block_fft_record<3, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,    1,   128,     0,  2082>
    >;
};

template<> struct block_fft_record<9, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    1,    64,     0,  2083>,
        block_fft_implementation< 3,    3,    3,    42,    36,  2084>,
        block_fft_implementation< 3,    3,    3,   128,    18,  2085>
    >;
};

template<> struct block_fft_record<27, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    1,    64,     0,  2086>,
        block_fft_implementation< 9,    9,    3,    42,   108,  2088>,
        block_fft_implementation< 9,    9,    3,    42,    54,  2087>,
        block_fft_implementation< 3,    3,    9,    56,   108,  2089>,
        block_fft_implementation< 3,    3,    9,    56,    54,  2090>
    >;
};

template<> struct block_fft_record<81, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    9,    14,   324,  2091>,
        block_fft_implementation< 9,    9,    9,    14,   162,  2092>,
        block_fft_implementation<27,   27,    3,    42,   324,  2094>,
        block_fft_implementation<27,   27,    3,    42,   162,  2093>,
        block_fft_implementation< 3,    3,   27,    14,   324,  2095>,
        block_fft_implementation< 3,    3,   27,    28,   162,  2096>
    >;
};

template<> struct block_fft_record<243, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    9,    14,   972,  2097>,
        block_fft_implementation<27,   27,    9,    14,   486,  2098>,
        block_fft_implementation< 9,    9,   27,    28,   972,  2099>,
        block_fft_implementation< 9,    9,   27,    18,   486,  2100>,
        block_fft_implementation< 3,    3,   81,     6,   972,  2101>,
        block_fft_implementation< 3,    3,   81,     6,   486,  2102>
    >;
};

template<> struct block_fft_record<729, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,   27,    28,  2916,  2103>,
        block_fft_implementation<27,   27,   27,    18,  1458,  2104>,
        block_fft_implementation< 9,    9,   81,     6,  2916,  2105>,
        block_fft_implementation< 9,    9,   81,     6,  1458,  2106>,
        block_fft_implementation< 3,    3,  243,     2,  2916,  2107>,
        block_fft_implementation< 3,    3,  243,     2,  1458,  2108>
    >;
};

template<> struct block_fft_record<2187, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,   81,     6,  8748,  2110>,
        block_fft_implementation< 9,    9,  243,     2,  8748,  2109>,
        block_fft_implementation< 9,    9,  243,     2,  4374,  2111>,
        block_fft_implementation<27,   27,   81,     6,  4374,  2112>,
        block_fft_implementation< 3,    3,  729,     2,  8748,  2113>,
        block_fft_implementation< 3,    3,  729,     2,  4374,  2114>
    >;
};

template<> struct block_fft_record<6561, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,  243,     2, 26244,  2116>,
        block_fft_implementation<27,   27,  243,     2, 13122,  2115>,
        block_fft_implementation< 9,    9,  729,     2, 26244,  2118>,
        block_fft_implementation< 9,    9,  729,     2, 13122,  2117>
    >;
};

template<> struct block_fft_record<19683, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,  729,     2, 78732,  3035>,
        block_fft_implementation<27,   27,  729,     2, 39366,  2119>
    >;
};

template<> struct block_fft_record<5, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,    1,   128,     0,  2120>
    >;
};

template<> struct block_fft_record<25, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    1,    64,     0,  2121>,
        block_fft_implementation< 5,    5,    5,    50,   100,  2122>,
        block_fft_implementation< 5,    5,    5,    50,    50,  2123>
    >;
};

template<> struct block_fft_record<125, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    5,    12,   500,  2125>,
        block_fft_implementation<25,   25,    5,    50,   250,  2124>,
        block_fft_implementation< 5,    5,   25,    10,   500,  2126>,
        block_fft_implementation< 5,    5,   25,    10,   250,  2127>
    >;
};

template<> struct block_fft_record<625, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,   25,    10,  2500,  2129>,
        block_fft_implementation<25,   25,   25,    10,  1250,  2128>,
        block_fft_implementation< 5,    5,  125,     2,  2500,  2130>,
        block_fft_implementation< 5,    5,  125,     2,  1250,  2131>
    >;
};

template<> struct block_fft_record<3125, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,  125,     2, 12500,  2133>,
        block_fft_implementation<25,   25,  125,     2,  6250,  2132>,
        block_fft_implementation< 5,    5,  625,     2, 12500,  2134>,
        block_fft_implementation< 5,    5,  625,     2,  6250,  2135>
    >;
};

template<> struct block_fft_record<15625, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,  625,     2, 62500,  3036>,
        block_fft_implementation<25,   25,  625,     2, 31250,  2136>
    >;
};

template<> struct block_fft_record<7, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    1,   128,     0,  2137>
    >;
};

template<> struct block_fft_record<49, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<49,   49,    1,   128,     0,  2138>,
        block_fft_implementation< 7,    7,    7,    18,   196,  2139>,
        block_fft_implementation< 7,    7,    7,    18,    98,  2140>
    >;
};

template<> struct block_fft_record<343, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,   49,    10,  1372,  2141>,
        block_fft_implementation< 7,    7,   49,    10,   686,  2142>
    >;
};

template<> struct block_fft_record<2401, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,  343,     2,  9604,  2143>,
        block_fft_implementation< 7,    7,  343,     2,  4802,  2144>
    >;
};

template<> struct block_fft_record<16807, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<49,   49,  343,     2, 67228,  3037>,
        block_fft_implementation<49,   49,  343,     2, 33614,  2145>
    >;
};

template<> struct block_fft_record<11, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,    1,    64,     0,  2146>
    >;
};

template<> struct block_fft_record<121, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,   11,    46,   484,  2147>,
        block_fft_implementation<11,   11,   11,    46,   242,  2148>
    >;
};

template<> struct block_fft_record<1331, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,  121,     2,  5324,  2150>,
        block_fft_implementation<11,   11,  121,     2,  2662,  2149>
    >;
};

template<> struct block_fft_record<6, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    1,   128,     0,  2151>
    >;
};

template<> struct block_fft_record<36, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    6,    42,   144,  2153>,
        block_fft_implementation< 6,    6,    6,    42,    72,  2152>,
        block_fft_implementation<36,   36,    1,    72,     0,  2154>
    >;
};

template<> struct block_fft_record<216, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,    6,    42,   432,  3038>,
        block_fft_implementation<36,   36,    6,    20,   864,  3039>,
        block_fft_implementation< 6,    6,   36,    14,   864,  2155>,
        block_fft_implementation< 6,    6,   36,    14,   432,  2156>
    >;
};

template<> struct block_fft_record<1296, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,   36,    14,  5184,  2158>,
        block_fft_implementation<36,   36,   36,    14,  2592,  2157>,
        block_fft_implementation< 6,    6,  216,     2,  5184,  2159>,
        block_fft_implementation< 6,    6,  216,     2,  2592,  2160>
    >;
};

template<> struct block_fft_record<7776, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,  216,     2, 31104,  2161>,
        block_fft_implementation<36,   36,  216,     2, 15552,  2162>
    >;
};

template<> struct block_fft_record<10, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,    1,    64,     0,  2163>
    >;
};

template<> struct block_fft_record<100, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,   10,     6,   400,  2165>,
        block_fft_implementation<10,   10,   10,     6,   200,  2164>
    >;
};

template<> struct block_fft_record<1000, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,  100,    10,  4000,  2166>,
        block_fft_implementation<10,   10,  100,    10,  2000,  2167>
    >;
};

template<> struct block_fft_record<10000, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10, 1000,     2, 40000,  2168>,
        block_fft_implementation<10,   10, 1000,     2, 20000,  2169>
    >;
};

template<> struct block_fft_record<12, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    1,    64,     0,  2170>
    >;
};

template<> struct block_fft_record<144, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,   12,    42,   576,  2171>,
        block_fft_implementation<12,   12,   12,    10,   288,  2172>
    >;
};

template<> struct block_fft_record<1728, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,  144,    14,  6912,  2173>,
        block_fft_implementation<12,   12,  144,     8,  3456,  2174>
    >;
};

template<> struct block_fft_record<13, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,    1,    64,     0,  2175>
    >;
};

template<> struct block_fft_record<169, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,   13,    38,   676,  2176>,
        block_fft_implementation<13,   13,   13,    38,   338,  2177>
    >;
};

template<> struct block_fft_record<2197, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,  169,     6,  8788,  2179>,
        block_fft_implementation<13,   13,  169,     6,  4394,  2178>
    >;
};

template<> struct block_fft_record<14, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,    1,    64,     0,  2180>
    >;
};

template<> struct block_fft_record<196, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,   14,    18,   784,  2181>,
        block_fft_implementation<14,   14,   14,    18,   392,  2182>
    >;
};

template<> struct block_fft_record<2744, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,  196,    10, 10976,  2183>,
        block_fft_implementation<14,   14,  196,    10,  5488,  2184>
    >;
};

template<> struct block_fft_record<15, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,    1,    64,     0,  2185>
    >;
};

template<> struct block_fft_record<225, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,   15,     4,   900,  2186>,
        block_fft_implementation<15,   15,   15,     4,   450,  2187>
    >;
};

template<> struct block_fft_record<3375, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,  225,     2, 13500,  2188>,
        block_fft_implementation<15,   15,  225,     2,  6750,  2189>
    >;
};

template<> struct block_fft_record<17, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,    1,    64,     0,  2190>
    >;
};

template<> struct block_fft_record<289, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,   17,    30,  1156,  2191>,
        block_fft_implementation<17,   17,   17,    30,   578,  2192>
    >;
};

template<> struct block_fft_record<4913, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,  289,     4, 19652,  2193>,
        block_fft_implementation<17,   17,  289,     4,  9826,  2194>
    >;
};

template<> struct block_fft_record<18, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    1,    64,     0,  2195>
    >;
};

template<> struct block_fft_record<324, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,   18,    14,  1296,  2196>,
        block_fft_implementation<18,   18,   18,    14,   648,  2197>
    >;
};

template<> struct block_fft_record<5832, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,  324,     2, 23328,  2198>,
        block_fft_implementation<18,   18,  324,     2, 11664,  2199>
    >;
};

template<> struct block_fft_record<19, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,    1,    64,     0,  2200>
    >;
};

template<> struct block_fft_record<361, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,   19,    40,  1444,  2201>,
        block_fft_implementation<19,   19,   19,    26,   722,  2202>
    >;
};

template<> struct block_fft_record<6859, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,  361,     2, 27436,  2203>,
        block_fft_implementation<19,   19,  361,     2, 13718,  2204>
    >;
};

template<> struct block_fft_record<20, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    1,    64,     0,  2205>
    >;
};

template<> struct block_fft_record<400, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   20,    38,  1600,  2206>,
        block_fft_implementation<20,   20,   20,    12,   800,  2207>
    >;
};

template<> struct block_fft_record<8000, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,  400,     2, 32000,  2209>,
        block_fft_implementation<20,   20,  400,     2, 16000,  2208>
    >;
};

template<> struct block_fft_record<21, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,    1,    64,     0,  2210>
    >;
};

template<> struct block_fft_record<441, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,   21,     6,  1764,  2211>,
        block_fft_implementation<21,   21,   21,     6,   882,  2212>
    >;
};

template<> struct block_fft_record<9261, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,  441,     2, 37044,  2214>,
        block_fft_implementation<21,   21,  441,     2, 18522,  2213>
    >;
};

template<> struct block_fft_record<22, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    1,    64,     0,  2215>
    >;
};

template<> struct block_fft_record<484, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,   22,    58,  1936,  2216>,
        block_fft_implementation<22,   22,   22,    22,   968,  2217>
    >;
};

template<> struct block_fft_record<10648, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,  484,     2, 42592,  2218>,
        block_fft_implementation<22,   22,  484,     2, 21296,  2219>
    >;
};

template<> struct block_fft_record<23, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,    1,    64,     0,  2220>
    >;
};

template<> struct block_fft_record<529, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,   23,    22,  2116,  2221>,
        block_fft_implementation<23,   23,   23,    22,  1058,  2222>
    >;
};

template<> struct block_fft_record<12167, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,  529,     2, 48668,  2223>,
        block_fft_implementation<23,   23,  529,     2, 24334,  2224>
    >;
};

template<> struct block_fft_record<24, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    1,    64,     0,  2225>
    >;
};

template<> struct block_fft_record<576, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   24,    10,  1152,  2226>,
        block_fft_implementation<24,   24,   24,    10,  2304,  2227>
    >;
};

template<> struct block_fft_record<13824, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,  576,     2, 55296,  3040>,
        block_fft_implementation<24,   24,  576,     2, 27648,  2228>
    >;
};

template<> struct block_fft_record<26, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    1,    64,     0,  2229>
    >;
};

template<> struct block_fft_record<676, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   26,    38,  2704,  2230>,
        block_fft_implementation<26,   26,   26,    38,  1352,  2231>
    >;
};

template<> struct block_fft_record<17576, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,  676,     2, 70304,  3041>,
        block_fft_implementation<26,   26,  676,     2, 35152,  2232>
    >;
};

template<> struct block_fft_record<28, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    1,    64,     0,  2233>
    >;
};

template<> struct block_fft_record<784, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   28,    18,  1568,  2234>,
        block_fft_implementation<28,   28,   28,     2,  3136,  2235>
    >;
};

template<> struct block_fft_record<21952, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,  784,     2, 43904,  2236>
    >;
};

template<> struct block_fft_record<29, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,    1,    64,     0,  2237>
    >;
};

template<> struct block_fft_record<841, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,   29,    26,  3364,  2238>,
        block_fft_implementation<29,   29,   29,    26,  1682,  2239>
    >;
};

template<> struct block_fft_record<24389, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,  841,     2, 48778,  2240>
    >;
};

template<> struct block_fft_record<30, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    1,    64,     0,  2241>
    >;
};

template<> struct block_fft_record<900, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   30,    34,  3600,  2242>,
        block_fft_implementation<30,   30,   30,     2,  1800,  2243>
    >;
};

template<> struct block_fft_record<27000, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,  900,     2, 54000,  3042>
    >;
};

template<> struct block_fft_record<31, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,    1,    64,     0,  2244>
    >;
};

template<> struct block_fft_record<961, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,   31,    24,  3844,  2245>,
        block_fft_implementation<31,   31,   31,    16,  1922,  2246>
    >;
};

template<> struct block_fft_record<29791, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,  961,     2, 59582,  3043>
    >;
};

template<> struct block_fft_record<68, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    2,    32,   272,  2248>,
        block_fft_implementation<34,   34,    2,    64,   136,  2247>
    >;
};

template<> struct block_fft_record<72, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    6,    20,   288,  2250>,
        block_fft_implementation<12,   12,    6,    42,   144,  2249>,
        block_fft_implementation<24,   24,    3,    42,   144,  2251>,
        block_fft_implementation<36,   36,    2,    32,   144,  2252>,
        block_fft_implementation<36,   36,    2,    64,   288,  2258>,
        block_fft_implementation<24,   24,    3,    40,   288,  2253>,
        block_fft_implementation<18,   18,    4,    32,   288,  2256>,
        block_fft_implementation<18,   18,    4,    32,   144,  2255>,
        block_fft_implementation< 6,    6,   12,    16,   288,  2254>,
        block_fft_implementation< 6,    6,   12,    32,   144,  2257>
    >;
};

template<> struct block_fft_record<76, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    2,    64,   304,  2260>,
        block_fft_implementation<38,   38,    2,    32,   152,  2259>
    >;
};

template<> struct block_fft_record<80, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    4,    32,   160,  2261>,
        block_fft_implementation<20,   20,    4,    30,   320,  2262>,
        block_fft_implementation<40,   40,    2,    56,   160,  2263>,
        block_fft_implementation<40,   40,    2,    60,   320,  2266>,
        block_fft_implementation<10,   10,    8,    32,   320,  2264>,
        block_fft_implementation<10,   10,    8,    32,   160,  2265>
    >;
};

template<> struct block_fft_record<84, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    2,    32,   336,  2268>,
        block_fft_implementation<42,   42,    2,    32,   168,  2267>
    >;
};

template<> struct block_fft_record<88, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    2,    32,   176,  2269>,
        block_fft_implementation<44,   44,    2,    32,   352,  2272>,
        block_fft_implementation<22,   22,    4,    16,   352,  2271>,
        block_fft_implementation<22,   22,    4,    16,   176,  2270>
    >;
};

template<> struct block_fft_record<92, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    2,    32,   368,  2274>,
        block_fft_implementation<46,   46,    2,    32,   184,  2273>
    >;
};

template<> struct block_fft_record<96, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    4,    30,   384,  2275>,
        block_fft_implementation<12,   12,    8,    16,   384,  2276>,
        block_fft_implementation<24,   24,    4,    30,   192,  2277>,
        block_fft_implementation< 6,    6,   16,    16,   384,  2278>,
        block_fft_implementation<12,   12,    8,    32,   192,  2279>,
        block_fft_implementation<48,   48,    2,    60,   384,  2281>,
        block_fft_implementation< 6,    6,   16,    28,   192,  2280>,
        block_fft_implementation<48,   48,    2,    60,   192,  2282>
    >;
};

template<> struct block_fft_record<104, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    2,    32,   208,  2283>,
        block_fft_implementation<52,   52,    2,    64,   416,  2286>,
        block_fft_implementation<26,   26,    4,    16,   416,  2285>,
        block_fft_implementation<26,   26,    4,    16,   208,  2284>
    >;
};

template<> struct block_fft_record<108, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<54,   54,    2,    32,   216,  2290>,
        block_fft_implementation<36,   36,    3,    42,   216,  2289>,
        block_fft_implementation<18,   18,    6,    10,   432,  2287>,
        block_fft_implementation<54,   54,    2,    32,   432,  2296>,
        block_fft_implementation<18,   18,    6,    42,   216,  2288>,
        block_fft_implementation<36,   36,    3,    42,   432,  2293>,
        block_fft_implementation< 6,    6,   18,    14,   432,  2291>,
        block_fft_implementation<12,   12,    9,    14,   216,  2294>,
        block_fft_implementation< 6,    6,   18,    14,   216,  2292>,
        block_fft_implementation<12,   12,    9,    14,   432,  2295>
    >;
};

template<> struct block_fft_record<112, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    4,    16,   224,  2297>,
        block_fft_implementation<28,   28,    4,    32,   448,  2298>,
        block_fft_implementation<56,   56,    2,    64,   224,  2299>,
        block_fft_implementation<56,   56,    2,    56,   448,  2302>,
        block_fft_implementation<14,   14,    8,    16,   448,  2300>,
        block_fft_implementation<14,   14,    8,    16,   224,  2301>
    >;
};

template<> struct block_fft_record<116, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    2,    32,   464,  2304>,
        block_fft_implementation<58,   58,    2,    64,   232,  2303>
    >;
};

template<> struct block_fft_record<120, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    2,    32,   240,  2305>,
        block_fft_implementation<60,   60,    2,    56,   480,  2308>,
        block_fft_implementation<30,   30,    4,    16,   480,  2307>,
        block_fft_implementation<30,   30,    4,    16,   240,  2306>
    >;
};

template<> struct block_fft_record<124, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    2,    64,   496,  2310>,
        block_fft_implementation<62,   62,    2,    32,   248,  2309>
    >;
};

template<> struct block_fft_record<136, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    4,    16,   544,  2312>,
        block_fft_implementation<34,   34,    4,    16,   272,  2311>
    >;
};

template<> struct block_fft_record<152, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    4,    16,   608,  2313>,
        block_fft_implementation<38,   38,    4,    16,   304,  2314>
    >;
};

template<> struct block_fft_record<160, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    4,    30,   640,  2317>,
        block_fft_implementation<20,   20,    8,    16,   640,  2315>,
        block_fft_implementation<40,   40,    4,    30,   320,  2316>,
        block_fft_implementation<10,   10,   16,     8,   640,  2318>,
        block_fft_implementation<20,   20,    8,    16,   320,  2319>,
        block_fft_implementation<10,   10,   16,    16,   320,  2320>
    >;
};

template<> struct block_fft_record<168, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    4,    16,   672,  2322>,
        block_fft_implementation<42,   42,    4,    16,   336,  2321>
    >;
};

template<> struct block_fft_record<176, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    4,    16,   352,  2323>,
        block_fft_implementation<44,   44,    4,    16,   704,  2324>,
        block_fft_implementation<22,   22,    8,     8,   704,  2325>,
        block_fft_implementation<22,   22,    8,     8,   352,  2326>
    >;
};

template<> struct block_fft_record<180, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    6,    42,   720,  2328>,
        block_fft_implementation<30,   30,    6,    42,   360,  2327>,
        block_fft_implementation<60,   60,    3,    42,   360,  2329>,
        block_fft_implementation<60,   60,    3,    42,   720,  2330>
    >;
};

template<> struct block_fft_record<184, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    4,    16,   736,  2331>,
        block_fft_implementation<46,   46,    4,    16,   368,  2332>
    >;
};

template<> struct block_fft_record<192, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    8,    16,   768,  2334>,
        block_fft_implementation<24,   24,    8,    16,   384,  2333>,
        block_fft_implementation<12,   12,   16,     8,   768,  2335>,
        block_fft_implementation<12,   12,   16,     8,   384,  2336>,
        block_fft_implementation<48,   48,    4,    30,   384,  2337>,
        block_fft_implementation<48,   48,    4,    16,   768,  2339>,
        block_fft_implementation< 6,    6,   32,     8,   768,  2338>,
        block_fft_implementation< 6,    6,   32,     8,   384,  2340>
    >;
};

template<> struct block_fft_record<200, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   10,     6,   800,  2341>,
        block_fft_implementation<20,   20,   10,    12,   400,  2342>,
        block_fft_implementation<40,   40,    5,    12,   400,  2343>,
        block_fft_implementation<40,   40,    5,    24,   800,  2346>,
        block_fft_implementation<10,   10,   20,     6,   800,  2344>,
        block_fft_implementation<50,   50,    4,    16,   800,  2348>,
        block_fft_implementation<10,   10,   20,     6,   400,  2345>,
        block_fft_implementation<50,   50,    4,    16,   400,  2347>
    >;
};

template<> struct block_fft_record<208, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    4,    32,   832,  2350>,
        block_fft_implementation<52,   52,    4,    16,   416,  2349>,
        block_fft_implementation<26,   26,    8,     8,   832,  2351>,
        block_fft_implementation<26,   26,    8,     8,   416,  2352>
    >;
};

template<> struct block_fft_record<224, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    4,    28,   896,  2356>,
        block_fft_implementation<28,   28,    8,     8,   896,  2353>,
        block_fft_implementation<56,   56,    4,    32,   448,  2354>,
        block_fft_implementation<14,   14,   16,     4,   896,  2355>,
        block_fft_implementation<28,   28,    8,    16,   448,  2357>,
        block_fft_implementation<14,   14,   16,     8,   448,  2358>
    >;
};

template<> struct block_fft_record<232, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    4,    16,   928,  2360>,
        block_fft_implementation<58,   58,    4,    16,   464,  2359>
    >;
};

template<> struct block_fft_record<240, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    4,    16,   480,  2361>,
        block_fft_implementation<60,   60,    4,    28,   960,  2362>,
        block_fft_implementation<30,   30,    8,     8,   960,  2363>,
        block_fft_implementation<30,   30,    8,     8,   480,  2364>
    >;
};

template<> struct block_fft_record<248, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    4,    16,   992,  2366>,
        block_fft_implementation<62,   62,    4,   128,   496,  2365>
    >;
};

template<> struct block_fft_record<252, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    6,    42,   504,  2367>,
        block_fft_implementation<42,   42,    6,    10,  1008,  2368>
    >;
};

template<> struct block_fft_record<272, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    8,     8,  1088,  2369>,
        block_fft_implementation<34,   34,    8,     8,   544,  2370>
    >;
};

template<> struct block_fft_record<288, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   12,    10,   576,  2371>,
        block_fft_implementation<24,   24,   12,    10,  1152,  2372>,
        block_fft_implementation<12,   12,   24,     8,  1152,  2373>,
        block_fft_implementation<36,   36,    8,     8,  1152,  2377>,
        block_fft_implementation<12,   12,   24,     8,   576,  2374>,
        block_fft_implementation<48,   48,    6,    10,   576,  2375>,
        block_fft_implementation<18,   18,   16,     4,  1152,  2376>,
        block_fft_implementation< 6,    6,   48,     4,  1152,  2378>,
        block_fft_implementation<48,   48,    6,    10,  1152,  2381>,
        block_fft_implementation<36,   36,    8,     8,   576,  2380>,
        block_fft_implementation< 6,    6,   48,     4,   576,  2379>,
        block_fft_implementation<18,   18,   16,     8,   576,  2382>
    >;
};

template<> struct block_fft_record<300, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   10,     6,  1200,  2384>,
        block_fft_implementation<30,   30,   10,    50,   600,  2383>,
        block_fft_implementation<60,   60,    5,    50,   600,  2385>,
        block_fft_implementation<60,   60,    5,    24,  1200,  2386>
    >;
};

template<> struct block_fft_record<304, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    8,     8,  1216,  2387>,
        block_fft_implementation<38,   38,    8,     8,   608,  2388>
    >;
};

template<> struct block_fft_record<320, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    8,    64,   640,  2389>,
        block_fft_implementation<40,   40,    8,    62,  1280,  2392>,
        block_fft_implementation<20,   20,   16,     4,  1280,  2390>,
        block_fft_implementation<20,   20,   16,     4,   640,  2391>,
        block_fft_implementation<10,   10,   32,     4,  1280,  2393>,
        block_fft_implementation<10,   10,   32,     8,   640,  2394>
    >;
};

template<> struct block_fft_record<336, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    8,     8,  1344,  2395>,
        block_fft_implementation<42,   42,    8,    32,   672,  2396>
    >;
};

template<> struct block_fft_record<352, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    8,     8,  1408,  2397>,
        block_fft_implementation<22,   22,   16,     4,  1408,  2398>,
        block_fft_implementation<44,   44,    8,     8,   704,  2399>,
        block_fft_implementation<22,   22,   16,     8,   704,  2400>
    >;
};

template<> struct block_fft_record<360, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    6,    42,   720,  2401>,
        block_fft_implementation<60,   60,    6,    20,  1440,  2403>,
        block_fft_implementation<30,   30,   12,    10,  1440,  2404>,
        block_fft_implementation<30,   30,   12,    10,   720,  2402>
    >;
};

template<> struct block_fft_record<368, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    8,     8,  1472,  2406>,
        block_fft_implementation<46,   46,    8,     8,   736,  2405>
    >;
};

template<> struct block_fft_record<384, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<48,   48,    8,    16,   768,  2410>,
        block_fft_implementation<24,   24,   16,     8,  1536,  2411>,
        block_fft_implementation<24,   24,   16,     4,   768,  2409>,
        block_fft_implementation<12,   12,   32,     2,  1536,  2407>,
        block_fft_implementation<12,   12,   32,     4,   768,  2408>,
        block_fft_implementation<48,   48,    8,     8,  1536,  2412>,
        block_fft_implementation< 6,    6,   64,     4,  1536,  2413>,
        block_fft_implementation< 6,    6,   64,     4,   768,  2414>
    >;
};

template<> struct block_fft_record<392, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   14,    18,   784,  2415>,
        block_fft_implementation<28,   28,   14,    18,  1568,  2416>,
        block_fft_implementation<56,   56,    7,    18,   784,  2418>,
        block_fft_implementation<56,   56,    7,     8,  1568,  2420>,
        block_fft_implementation<14,   14,   28,     2,  1568,  2417>,
        block_fft_implementation<14,   14,   28,     2,   784,  2419>
    >;
};

template<> struct block_fft_record<416, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    8,     8,  1664,  2421>,
        block_fft_implementation<26,   26,   16,     4,  1664,  2422>,
        block_fft_implementation<52,   52,    8,     8,   832,  2423>,
        block_fft_implementation<26,   26,   16,     4,   832,  2424>
    >;
};

template<> struct block_fft_record<432, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,   12,    42,  1728,  2427>,
        block_fft_implementation<36,   36,   12,    10,   864,  2425>,
        block_fft_implementation<12,   12,   36,    14,  1728,  2426>,
        block_fft_implementation<12,   12,   36,    14,   864,  2428>,
        block_fft_implementation<24,   24,   18,    14,   864,  2429>,
        block_fft_implementation< 6,    6,   72,     8,  1728,  2431>,
        block_fft_implementation<18,   18,   24,    10,  1728,  2430>,
        block_fft_implementation<24,   24,   18,    14,  1728,  2432>,
        block_fft_implementation< 6,    6,   72,     6,   864,  2433>,
        block_fft_implementation<48,   48,    9,    14,   864,  2435>,
        block_fft_implementation<18,   18,   24,    10,   864,  2434>,
        block_fft_implementation<54,   54,    8,     8,  1728,  2436>,
        block_fft_implementation<54,   54,    8,     8,   864,  2438>,
        block_fft_implementation<48,   48,    9,    14,  1728,  2437>
    >;
};

template<> struct block_fft_record<448, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    8,    14,  1792,  2442>,
        block_fft_implementation<56,   56,    8,     8,   896,  2441>,
        block_fft_implementation<28,   28,   16,     4,  1792,  2439>,
        block_fft_implementation<28,   28,   16,     4,   896,  2440>,
        block_fft_implementation<14,   14,   32,     4,  1792,  2443>,
        block_fft_implementation<14,   14,   32,     4,   896,  2444>
    >;
};

template<> struct block_fft_record<464, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    8,     8,  1856,  2446>,
        block_fft_implementation<58,   58,    8,    16,   928,  2445>
    >;
};

template<> struct block_fft_record<480, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    8,     8,  1920,  2448>,
        block_fft_implementation<30,   30,   16,     4,  1920,  2447>,
        block_fft_implementation<60,   60,    8,     8,   960,  2449>,
        block_fft_implementation<30,   30,   16,     8,   960,  2450>
    >;
};

template<> struct block_fft_record<496, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    8,     8,  1984,  2452>,
        block_fft_implementation<62,   62,    8,    64,   992,  2451>
    >;
};

template<> struct block_fft_record<500, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<50,   50,   10,     6,  2000,  2458>,
        block_fft_implementation<50,   50,   10,     6,  1000,  2457>,
        block_fft_implementation<10,   10,   50,    10,  2000,  2453>,
        block_fft_implementation<20,   20,   25,    10,  2000,  2455>,
        block_fft_implementation<20,   20,   25,    10,  1000,  2456>,
        block_fft_implementation<10,   10,   50,    10,  1000,  2454>
    >;
};

template<> struct block_fft_record<504, half, fft_type::c2c, fft_direction::forward, 800> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,   12,    10,  2016,  2459>,
        block_fft_implementation<42,   42,   12,    10,  1008,  2460>
    >;
};
