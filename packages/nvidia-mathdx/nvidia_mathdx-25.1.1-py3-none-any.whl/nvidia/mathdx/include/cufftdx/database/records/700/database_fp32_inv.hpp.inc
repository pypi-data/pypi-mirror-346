//Copyright (c) 2019-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
//NVIDIA CORPORATION and its licensors retain all intellectual property
//and proprietary rights in and to this software, related documentation
//and any modifications thereto.  Any use, reproduction, disclosure or
//distribution of this software and related documentation without an express
//license agreement from NVIDIA CORPORATION is strictly prohibited.
//


template<> struct block_fft_record<33, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<33,   33,    1,    32,     0,   511>
    >;
};

template<> struct block_fft_record<34, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    1,    32,     0,   512>
    >;
};

template<> struct block_fft_record<35, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<35,   35,    1,    32,     0,   513>
    >;
};

template<> struct block_fft_record<37, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<37,   37,    1,    32,     0,   514>
    >;
};

template<> struct block_fft_record<38, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    1,    32,     0,   515>
    >;
};

template<> struct block_fft_record<39, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<39,   39,    1,    32,     0,   516>
    >;
};

template<> struct block_fft_record<40, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    2,    32,   160,   517>,
        block_fft_implementation<10,   10,    4,    32,   320,   518>,
        block_fft_implementation<10,   10,    4,    32,   160,   519>,
        block_fft_implementation<40,   40,    1,    32,     0,   520>
    >;
};

template<> struct block_fft_record<41, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<41,   41,    1,    32,     0,   521>
    >;
};

template<> struct block_fft_record<42, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    1,    32,     0,   522>
    >;
};

template<> struct block_fft_record<43, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<43,   43,    1,    32,     0,   523>
    >;
};

template<> struct block_fft_record<44, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    1,    32,     0,   524>
    >;
};

template<> struct block_fft_record<45, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<45,   45,    1,    32,     0,   525>
    >;
};

template<> struct block_fft_record<46, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    1,    32,     0,   526>
    >;
};

template<> struct block_fft_record<47, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<47,   47,    1,    32,     0,   527>
    >;
};

template<> struct block_fft_record<48, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<48,   48,    1,    32,     0,   528>
    >;
};

template<> struct block_fft_record<50, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<50,   50,    1,    32,     0,   529>
    >;
};

template<> struct block_fft_record<51, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<51,   51,    1,    32,     0,   530>
    >;
};

template<> struct block_fft_record<52, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    1,    32,     0,   531>
    >;
};

template<> struct block_fft_record<53, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<53,   53,    1,    32,     0,   532>
    >;
};

template<> struct block_fft_record<54, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<54,   54,    1,    32,     0,   533>
    >;
};

template<> struct block_fft_record<55, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<55,   55,    1,    32,     0,   534>
    >;
};

template<> struct block_fft_record<56, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    1,    32,     0,   535>
    >;
};

template<> struct block_fft_record<57, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<57,   57,    1,    32,     0,   536>
    >;
};

template<> struct block_fft_record<58, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    1,    32,     0,   537>
    >;
};

template<> struct block_fft_record<59, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<59,   59,    1,    32,     0,   538>
    >;
};

template<> struct block_fft_record<60, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    1,    32,     0,   539>
    >;
};

template<> struct block_fft_record<61, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<61,   61,    1,    32,     0,   540>
    >;
};

template<> struct block_fft_record<62, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    1,    32,     0,   541>
    >;
};

template<> struct block_fft_record<63, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<63,   63,    1,    32,     0,   542>
    >;
};

template<> struct block_fft_record<2, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 2,    2,    1,    64,     0,   543>
    >;
};

template<> struct block_fft_record<4, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4,    1,    64,     0,   544>,
        block_fft_implementation< 2,    2,    2,   128,    16,   545>,
        block_fft_implementation< 2,    2,    2,   128,    32,   546>
    >;
};

template<> struct block_fft_record<8, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    1,    32,     0,   547>,
        block_fft_implementation< 4,    4,    2,   128,    32,   548>,
        block_fft_implementation< 4,    4,    2,    96,    64,   549>,
        block_fft_implementation< 2,    2,    4,    80,    32,   550>,
        block_fft_implementation< 2,    2,    4,   128,    64,   551>
    >;
};

template<> struct block_fft_record<16, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    1,   112,     0,   552>,
        block_fft_implementation< 4,    4,    4,    64,    64,   553>,
        block_fft_implementation< 4,    4,    4,    96,   128,   554>,
        block_fft_implementation< 8,    8,    2,   128,    64,   555>,
        block_fft_implementation< 8,    8,    2,   112,   128,   556>,
        block_fft_implementation< 2,    2,    8,    64,    64,   557>,
        block_fft_implementation< 2,    2,    8,    64,   128,   558>
    >;
};

template<> struct block_fft_record<32, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,    1,    32,     0,   559>,
        block_fft_implementation< 8,    8,    4,    48,   256,   560>,
        block_fft_implementation< 8,    8,    4,    96,   128,   561>,
        block_fft_implementation< 4,    4,    8,    48,   256,   562>,
        block_fft_implementation< 4,    4,    8,    64,   128,   563>,
        block_fft_implementation< 2,    2,   16,    20,   256,   564>,
        block_fft_implementation<16,   16,    2,    64,   256,   565>,
        block_fft_implementation< 2,    2,   16,    26,   128,   566>,
        block_fft_implementation<16,   16,    2,   128,   128,   567>
    >;
};

template<> struct block_fft_record<64, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    8,    24,   512,   568>,
        block_fft_implementation< 8,    8,    8,    13,   256,   569>,
        block_fft_implementation< 4,    4,   16,     9,   512,   570>,
        block_fft_implementation< 4,    4,   16,    15,   256,   571>,
        block_fft_implementation<16,   16,    4,    25,   512,   572>,
        block_fft_implementation<16,   16,    4,    29,   256,   573>,
        block_fft_implementation<32,   32,    2,    23,   512,   574>,
        block_fft_implementation< 2,    2,   32,    14,   512,   575>,
        block_fft_implementation< 2,    2,   32,     8,   256,   576>,
        block_fft_implementation<32,   32,    2,    64,   256,   577>,
        block_fft_implementation<64,   64,    1,    32,     0,   578>
    >;
};

template<> struct block_fft_record<128, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    8,    16,   512,   579>,
        block_fft_implementation< 8,    8,   16,     8,  1024,   580>,
        block_fft_implementation<16,   16,    8,    13,  1024,   581>,
        block_fft_implementation< 8,    8,   16,    16,   512,   582>,
        block_fft_implementation< 4,    4,   32,     4,  1024,   583>,
        block_fft_implementation< 4,    4,   32,     7,   512,   584>,
        block_fft_implementation<32,   32,    4,     4,  1024,   585>,
        block_fft_implementation<32,   32,    4,    31,   512,   586>,
        block_fft_implementation< 2,    2,   64,     6,  1024,   587>,
        block_fft_implementation< 2,    2,   64,     6,   512,   588>
    >;
};

template<> struct block_fft_record<256, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,   16,     2,  1024,   589>,
        block_fft_implementation< 8,    8,   32,     4,  2048,   590>,
        block_fft_implementation< 8,    8,   32,     4,  1024,   591>,
        block_fft_implementation<16,   16,   16,     3,  2048,   592>,
        block_fft_implementation<32,   32,    8,     4,  2048,   593>,
        block_fft_implementation< 4,    4,   64,     2,  2048,   594>,
        block_fft_implementation< 4,    4,   64,     4,  1024,   595>,
        block_fft_implementation<32,   32,    8,    16,  1024,   596>,
        block_fft_implementation< 2,    2,  128,     3,  2048,   597>,
        block_fft_implementation< 2,    2,  128,     4,  1024,   598>
    >;
};

template<> struct block_fft_record<512, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,   64,     2,  4096,   599>,
        block_fft_implementation< 8,    8,   64,     2,  2048,   600>,
        block_fft_implementation<16,   16,   32,     1,  2048,   601>,
        block_fft_implementation<32,   32,   16,     2,  4096,   602>,
        block_fft_implementation<32,   32,   16,     2,  2048,   603>,
        block_fft_implementation<16,   16,   32,     4,  4096,   604>,
        block_fft_implementation< 4,    4,  128,     2,  4096,   605>,
        block_fft_implementation< 4,    4,  128,     2,  2048,   606>,
        block_fft_implementation< 2,    2,  256,     1,  4096,   607>,
        block_fft_implementation< 2,    2,  256,     2,  2048,   608>
    >;
};

template<> struct block_fft_record<1024, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,   64,     1,  4096,   609>,
        block_fft_implementation< 8,    8,  128,     1,  8192,   610>,
        block_fft_implementation<32,   32,   32,     4,  8192,   611>,
        block_fft_implementation< 8,    8,  128,     1,  4096,   612>,
        block_fft_implementation<32,   32,   32,     4,  4096,   613>,
        block_fft_implementation<16,   16,   64,     2,  8192,   614>,
        block_fft_implementation< 4,    4,  256,     1,  8192,   615>,
        block_fft_implementation< 4,    4,  256,     1,  4096,   616>,
        block_fft_implementation< 2,    2,  512,     1,  8192,   617>,
        block_fft_implementation< 2,    2,  512,     1,  4096,   618>
    >;
};

template<> struct block_fft_record<2048, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  128,     1,  8192,   619>,
        block_fft_implementation< 8,    8,  256,     1, 16384,   620>,
        block_fft_implementation< 8,    8,  256,     1,  8192,   621>,
        block_fft_implementation<16,   16,  128,     1, 16384,   622>,
        block_fft_implementation<32,   32,   64,     2, 16384,   623>,
        block_fft_implementation<32,   32,   64,     2,  8192,   624>,
        block_fft_implementation< 4,    4,  512,     1, 16384,   625>,
        block_fft_implementation< 4,    4,  512,     1,  8192,   626>,
        block_fft_implementation< 2,    2, 1024,     1, 16384,   627>,
        block_fft_implementation< 2,    2, 1024,     1,  8192,   628>
    >;
};

template<> struct block_fft_record<4096, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  256,     1, 16384,   629>,
        block_fft_implementation< 8,    8,  512,     1, 32768,   630>,
        block_fft_implementation< 8,    8,  512,     1, 16384,   631>,
        block_fft_implementation<16,   16,  256,     1, 32768,   632>,
        block_fft_implementation<32,   32,  128,     1, 32768,   633>,
        block_fft_implementation<32,   32,  128,     1, 16384,   634>,
        block_fft_implementation< 4,    4, 1024,     1, 32768,   635>,
        block_fft_implementation< 4,    4, 1024,     1, 16384,   636>
    >;
};

template<> struct block_fft_record<8192, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  512,     1, 32768,   637>,
        block_fft_implementation<32,   32,  256,     1, 65536,   638>,
        block_fft_implementation<32,   32,  256,     1, 32768,   639>,
        block_fft_implementation< 8,    8, 1024,     1, 65536,   640>,
        block_fft_implementation<16,   16,  512,     1, 65536,   641>,
        block_fft_implementation< 8,    8, 1024,     1, 32768,   642>
    >;
};

template<> struct block_fft_record<16384, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16, 1024,     1, 65536,   643>,
        block_fft_implementation<32,   32,  512,     1, 65536,   644>
    >;
};

template<> struct block_fft_record<3, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,    1,    64,     0,   645>
    >;
};

template<> struct block_fft_record<9, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    1,    64,     0,   646>,
        block_fft_implementation< 3,    3,    3,    64,    72,   647>,
        block_fft_implementation< 3,    3,    3,   128,    36,   648>
    >;
};

template<> struct block_fft_record<27, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    1,    32,     0,   649>,
        block_fft_implementation< 9,    9,    3,    21,   108,   650>,
        block_fft_implementation< 9,    9,    3,    10,   216,   651>,
        block_fft_implementation< 3,    3,    9,    26,   216,   652>,
        block_fft_implementation< 3,    3,    9,    24,   108,   653>
    >;
};

template<> struct block_fft_record<81, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    9,    14,   648,   654>,
        block_fft_implementation< 9,    9,    9,     7,   324,   655>,
        block_fft_implementation<27,   27,    3,    10,   324,   656>,
        block_fft_implementation<27,   27,    3,     9,   648,   657>,
        block_fft_implementation< 3,    3,   27,     7,   648,   658>,
        block_fft_implementation< 3,    3,   27,     9,   324,   659>
    >;
};

template<> struct block_fft_record<243, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    9,    14,  1944,   660>,
        block_fft_implementation<27,   27,    9,    14,   972,   661>,
        block_fft_implementation< 9,    9,   27,     9,  1944,   662>,
        block_fft_implementation< 9,    9,   27,     9,   972,   663>,
        block_fft_implementation< 3,    3,   81,     3,  1944,   664>,
        block_fft_implementation< 3,    3,   81,     3,   972,   665>
    >;
};

template<> struct block_fft_record<729, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,   27,    14,  5832,   666>,
        block_fft_implementation<27,   27,   27,     9,  2916,   667>,
        block_fft_implementation< 9,    9,   81,     3,  5832,   668>,
        block_fft_implementation< 9,    9,   81,     3,  2916,   669>,
        block_fft_implementation< 3,    3,  243,     1,  5832,   670>,
        block_fft_implementation< 3,    3,  243,     1,  2916,   671>
    >;
};

template<> struct block_fft_record<2187, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,  243,     1, 17496,   672>,
        block_fft_implementation<27,   27,   81,     3, 17496,   673>,
        block_fft_implementation< 9,    9,  243,     1,  8748,   674>,
        block_fft_implementation<27,   27,   81,     3,  8748,   675>,
        block_fft_implementation< 3,    3,  729,     1, 17496,   676>,
        block_fft_implementation< 3,    3,  729,     1,  8748,   677>
    >;
};

template<> struct block_fft_record<6561, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,  243,     1, 26244,   678>,
        block_fft_implementation<27,   27,  243,     1, 52488,   679>,
        block_fft_implementation< 9,    9,  729,     1, 26244,   680>,
        block_fft_implementation< 9,    9,  729,     1, 52488,   681>
    >;
};

template<> struct block_fft_record<19683, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,  729,     1, 78732,   682>
    >;
};

template<> struct block_fft_record<5, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,    1,    32,     0,   683>
    >;
};

template<> struct block_fft_record<25, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    1,    32,     0,   684>,
        block_fft_implementation< 5,    5,    5,   128,   200,   685>,
        block_fft_implementation< 5,    5,    5,    25,   100,   686>
    >;
};

template<> struct block_fft_record<125, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    5,    25,   500,   687>,
        block_fft_implementation<25,   25,    5,    25,  1000,   688>,
        block_fft_implementation< 5,    5,   25,     5,  1000,   689>,
        block_fft_implementation< 5,    5,   25,     5,   500,   690>
    >;
};

template<> struct block_fft_record<625, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,   25,     5,  2500,   691>,
        block_fft_implementation<25,   25,   25,     5,  5000,   692>,
        block_fft_implementation< 5,    5,  125,     1,  5000,   693>,
        block_fft_implementation< 5,    5,  125,     1,  2500,   694>
    >;
};

template<> struct block_fft_record<3125, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,  125,     1, 12500,   695>,
        block_fft_implementation<25,   25,  125,     3, 25000,   696>,
        block_fft_implementation< 5,    5,  625,     1, 25000,   697>,
        block_fft_implementation< 5,    5,  625,     1, 12500,   698>
    >;
};

template<> struct block_fft_record<15625, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,  625,     1, 62500,   699>
    >;
};

template<> struct block_fft_record<7, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    1,    64,     0,   700>
    >;
};

template<> struct block_fft_record<49, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<49,   49,    1,    32,     0,   701>,
        block_fft_implementation< 7,    7,    7,     9,   392,   702>,
        block_fft_implementation< 7,    7,    7,     9,   196,   703>
    >;
};

template<> struct block_fft_record<343, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,   49,     5,  2744,   704>,
        block_fft_implementation< 7,    7,   49,     5,  1372,   705>
    >;
};

template<> struct block_fft_record<2401, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,  343,     1, 19208,   706>,
        block_fft_implementation< 7,    7,  343,     1,  9604,   707>
    >;
};

template<> struct block_fft_record<16807, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<49,   49,  343,     1, 67228,   708>
    >;
};

template<> struct block_fft_record<11, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,    1,    96,     0,   709>
    >;
};

template<> struct block_fft_record<121, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,   11,    23,   968,   710>,
        block_fft_implementation<11,   11,   11,    23,   484,   711>
    >;
};

template<> struct block_fft_record<1331, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,  121,     1,  5324,   712>,
        block_fft_implementation<11,   11,  121,     1, 10648,   713>
    >;
};

template<> struct block_fft_record<6, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    1,    32,     0,   714>
    >;
};

template<> struct block_fft_record<36, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    6,    64,   144,   715>,
        block_fft_implementation< 6,    6,    6,    64,   288,   716>,
        block_fft_implementation<36,   36,    1,    36,     0,   717>
    >;
};

template<> struct block_fft_record<216, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,   36,     7,  1728,   718>,
        block_fft_implementation< 6,    6,   36,     7,   864,   719>
    >;
};

template<> struct block_fft_record<1296, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,  216,     2, 10368,   720>,
        block_fft_implementation< 6,    6,  216,     1,  5184,   721>
    >;
};

template<> struct block_fft_record<7776, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,  216,     1, 62208,   722>,
        block_fft_implementation<36,   36,  216,     1, 31104,   723>
    >;
};

template<> struct block_fft_record<10, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,    1,    32,     0,   724>
    >;
};

template<> struct block_fft_record<100, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,   10,    25,   400,   725>,
        block_fft_implementation<10,   10,   10,    25,   800,   726>
    >;
};

template<> struct block_fft_record<1000, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,  100,     5,  8000,   727>,
        block_fft_implementation<10,   10,  100,     5,  4000,   728>
    >;
};

template<> struct block_fft_record<10000, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10, 1000,     1, 80000,   729>,
        block_fft_implementation<10,   10, 1000,     1, 40000,   730>
    >;
};

template<> struct block_fft_record<12, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    1,    64,     0,   731>
    >;
};

template<> struct block_fft_record<144, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,   12,    21,  1152,   732>,
        block_fft_implementation<12,   12,   12,    21,   576,   733>
    >;
};

template<> struct block_fft_record<1728, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,  144,     1, 13824,   734>,
        block_fft_implementation<12,   12,  144,     1,  6912,   735>
    >;
};

template<> struct block_fft_record<13, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,    1,    32,     0,   736>
    >;
};

template<> struct block_fft_record<169, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,   13,    19,  1352,   737>,
        block_fft_implementation<13,   13,   13,    19,   676,   738>
    >;
};

template<> struct block_fft_record<2197, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,  169,     3,  8788,   739>,
        block_fft_implementation<13,   13,  169,     2, 17576,   740>
    >;
};

template<> struct block_fft_record<14, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,    1,    32,     0,   741>
    >;
};

template<> struct block_fft_record<196, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,   14,     9,  1568,   742>,
        block_fft_implementation<14,   14,   14,     9,   784,   743>
    >;
};

template<> struct block_fft_record<2744, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,  196,     2, 21952,   744>,
        block_fft_implementation<14,   14,  196,     1, 10976,   745>
    >;
};

template<> struct block_fft_record<15, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,    1,    32,     0,   746>
    >;
};

template<> struct block_fft_record<225, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,   15,    17,  1800,   747>,
        block_fft_implementation<15,   15,   15,    17,   900,   748>
    >;
};

template<> struct block_fft_record<3375, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,  225,     1, 27000,   749>,
        block_fft_implementation<15,   15,  225,     1, 13500,   750>
    >;
};

template<> struct block_fft_record<17, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,    1,    32,     0,   751>
    >;
};

template<> struct block_fft_record<289, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,   17,    15,  2312,   752>,
        block_fft_implementation<17,   17,   17,    15,  1156,   753>
    >;
};

template<> struct block_fft_record<4913, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,  289,     2, 39304,   754>,
        block_fft_implementation<17,   17,  289,     2, 19652,   755>
    >;
};

template<> struct block_fft_record<18, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    1,    32,     0,   756>
    >;
};

template<> struct block_fft_record<324, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,   18,     7,  2592,   757>,
        block_fft_implementation<18,   18,   18,     7,  1296,   758>
    >;
};

template<> struct block_fft_record<5832, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,  324,     1, 46656,   759>,
        block_fft_implementation<18,   18,  324,     1, 23328,   760>
    >;
};

template<> struct block_fft_record<19, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,    1,    32,     0,   761>
    >;
};

template<> struct block_fft_record<361, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,   19,    13,  2888,   762>,
        block_fft_implementation<19,   19,   19,    13,  1444,   763>
    >;
};

template<> struct block_fft_record<6859, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,  361,     1, 54872,   764>,
        block_fft_implementation<19,   19,  361,     1, 27436,   765>
    >;
};

template<> struct block_fft_record<20, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    1,    32,     0,   766>
    >;
};

template<> struct block_fft_record<400, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   20,     6,  3200,   767>,
        block_fft_implementation<20,   20,   20,     6,  1600,   768>
    >;
};

template<> struct block_fft_record<8000, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,  400,     1, 32000,   769>,
        block_fft_implementation<20,   20,  400,     1, 64000,   770>
    >;
};

template<> struct block_fft_record<21, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,    1,    32,     0,   771>
    >;
};

template<> struct block_fft_record<441, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,   21,     6,  3528,   772>,
        block_fft_implementation<21,   21,   21,     6,  1764,   773>
    >;
};

template<> struct block_fft_record<9261, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,  441,     1, 37044,   774>,
        block_fft_implementation<21,   21,  441,     1, 74088,   775>
    >;
};

template<> struct block_fft_record<22, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    1,    32,     0,   776>
    >;
};

template<> struct block_fft_record<484, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,   22,    11,  3872,   777>,
        block_fft_implementation<22,   22,   22,    11,  1936,   778>
    >;
};

template<> struct block_fft_record<10648, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,  484,     1, 85184,   779>,
        block_fft_implementation<22,   22,  484,     1, 42592,   780>
    >;
};

template<> struct block_fft_record<23, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,    1,    32,     0,   781>
    >;
};

template<> struct block_fft_record<529, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,   23,    11,  4232,   782>,
        block_fft_implementation<23,   23,   23,    11,  2116,   783>
    >;
};

template<> struct block_fft_record<12167, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,  529,     1, 97336,   784>,
        block_fft_implementation<23,   23,  529,     1, 48668,   785>
    >;
};

template<> struct block_fft_record<24, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    1,    32,     0,   786>
    >;
};

template<> struct block_fft_record<576, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   24,     5,  2304,   787>,
        block_fft_implementation<24,   24,   24,     5,  4608,   788>
    >;
};

template<> struct block_fft_record<13824, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,  576,     1, 55296,   789>
    >;
};

template<> struct block_fft_record<26, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    1,    32,     0,   790>
    >;
};

template<> struct block_fft_record<676, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   26,    14,  5408,   791>,
        block_fft_implementation<26,   26,   26,     9,  2704,   792>
    >;
};

template<> struct block_fft_record<17576, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,  676,     1, 70304,   793>
    >;
};

template<> struct block_fft_record<28, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    1,    32,     0,   794>
    >;
};

template<> struct block_fft_record<784, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   28,     9,  3136,   795>,
        block_fft_implementation<28,   28,   28,     9,  6272,   796>
    >;
};

template<> struct block_fft_record<21952, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,  784,     1, 87808,   797>
    >;
};

template<> struct block_fft_record<29, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,    1,    32,     0,   798>
    >;
};

template<> struct block_fft_record<841, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,   29,    13,  6728,   799>,
        block_fft_implementation<29,   29,   29,    13,  3364,   800>
    >;
};

template<> struct block_fft_record<24389, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,  841,     1, 97556,   801>
    >;
};

template<> struct block_fft_record<30, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    1,    32,     0,   802>
    >;
};

template<> struct block_fft_record<900, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   30,     4,  7200,   803>,
        block_fft_implementation<30,   30,   30,     4,  3600,   804>
    >;
};

template<> struct block_fft_record<31, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,    1,    32,     0,   805>
    >;
};

template<> struct block_fft_record<961, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,   31,     8,  7688,   806>,
        block_fft_implementation<31,   31,   31,     8,  3844,   807>
    >;
};

template<> struct block_fft_record<68, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    2,    64,   272,   808>,
        block_fft_implementation<34,   34,    2,    16,   544,   809>
    >;
};

template<> struct block_fft_record<72, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    6,    21,   288,   810>,
        block_fft_implementation<24,   24,    3,    10,   288,   811>,
        block_fft_implementation<12,   12,    6,    21,   576,   812>,
        block_fft_implementation<36,   36,    2,    16,   288,   813>,
        block_fft_implementation<18,   18,    4,     8,   288,   814>,
        block_fft_implementation<24,   24,    3,    10,   576,   815>,
        block_fft_implementation<18,   18,    4,     8,   576,   816>,
        block_fft_implementation<36,   36,    2,    16,   576,   817>,
        block_fft_implementation< 6,    6,   12,     8,   288,   818>,
        block_fft_implementation< 6,    6,   12,    10,   576,   819>
    >;
};

template<> struct block_fft_record<76, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    2,    64,   304,   820>,
        block_fft_implementation<38,   38,    2,    64,   608,   821>
    >;
};

template<> struct block_fft_record<80, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    4,     8,   320,   822>,
        block_fft_implementation<20,   20,    4,     8,   640,   823>,
        block_fft_implementation<40,   40,    2,    16,   320,   824>,
        block_fft_implementation<40,   40,    2,    16,   640,   825>,
        block_fft_implementation<10,   10,    8,    16,   320,   826>,
        block_fft_implementation<10,   10,    8,     8,   640,   827>
    >;
};

template<> struct block_fft_record<84, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    2,    64,   336,   828>,
        block_fft_implementation<42,   42,    2,    64,   672,   829>
    >;
};

template<> struct block_fft_record<88, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    2,    64,   352,   830>,
        block_fft_implementation<22,   22,    4,     8,   352,   831>,
        block_fft_implementation<22,   22,    4,     8,   704,   832>,
        block_fft_implementation<44,   44,    2,    64,   704,   833>
    >;
};

template<> struct block_fft_record<92, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    2,    64,   368,   834>,
        block_fft_implementation<46,   46,    2,   128,   736,   835>
    >;
};

template<> struct block_fft_record<96, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    4,     8,   768,   836>,
        block_fft_implementation<12,   12,    8,     4,   768,   837>,
        block_fft_implementation<24,   24,    4,    32,   384,   838>,
        block_fft_implementation< 6,    6,   16,     8,   768,   839>,
        block_fft_implementation<12,   12,    8,    16,   384,   840>,
        block_fft_implementation<48,   48,    2,    32,   768,   841>,
        block_fft_implementation< 6,    6,   16,    14,   384,   842>,
        block_fft_implementation<48,   48,    2,    16,   384,   843>
    >;
};

template<> struct block_fft_record<104, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    2,    64,   416,   844>,
        block_fft_implementation<26,   26,    4,    32,   416,   845>,
        block_fft_implementation<26,   26,    4,     8,   832,   846>,
        block_fft_implementation<52,   52,    2,    14,   832,   847>
    >;
};

template<> struct block_fft_record<108, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    6,    21,   432,   848>,
        block_fft_implementation<18,   18,    6,    21,   864,   849>,
        block_fft_implementation<36,   36,    3,    10,   432,   850>,
        block_fft_implementation<54,   54,    2,    64,   432,   851>,
        block_fft_implementation< 6,    6,   18,     7,   432,   852>,
        block_fft_implementation<36,   36,    3,    10,   864,   853>,
        block_fft_implementation< 6,    6,   18,     7,   864,   854>,
        block_fft_implementation<12,   12,    9,     7,   432,   855>,
        block_fft_implementation<12,   12,    9,     3,   864,   856>,
        block_fft_implementation<54,   54,    2,   112,   864,   857>
    >;
};

template<> struct block_fft_record<112, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    4,     8,   448,   858>,
        block_fft_implementation<28,   28,    4,     8,   896,   859>,
        block_fft_implementation<56,   56,    2,    64,   448,   860>,
        block_fft_implementation<14,   14,    8,    16,   448,   861>,
        block_fft_implementation<14,   14,    8,     4,   896,   862>,
        block_fft_implementation<56,   56,    2,    48,   896,   863>
    >;
};

template<> struct block_fft_record<116, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    2,   128,   464,   864>,
        block_fft_implementation<58,   58,    2,    96,   928,   865>
    >;
};

template<> struct block_fft_record<120, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    2,    64,   480,   866>,
        block_fft_implementation<30,   30,    4,     8,   480,   867>,
        block_fft_implementation<30,   30,    4,     8,   960,   868>,
        block_fft_implementation<60,   60,    2,    96,   960,   869>
    >;
};

template<> struct block_fft_record<124, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    2,   128,   496,   870>,
        block_fft_implementation<62,   62,    2,    96,   992,   871>
    >;
};

template<> struct block_fft_record<136, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    4,    32,   544,   872>,
        block_fft_implementation<34,   34,    4,     8,  1088,   873>
    >;
};

template<> struct block_fft_record<152, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    4,    32,   608,   874>,
        block_fft_implementation<38,   38,    4,    32,  1216,   875>
    >;
};

template<> struct block_fft_record<160, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    8,     4,  1280,   876>,
        block_fft_implementation<40,   40,    4,     8,  1280,   877>,
        block_fft_implementation<40,   40,    4,     8,   640,   878>,
        block_fft_implementation<10,   10,   16,     2,  1280,   879>,
        block_fft_implementation<20,   20,    8,    16,   640,   880>,
        block_fft_implementation<10,   10,   16,     8,   640,   881>
    >;
};

template<> struct block_fft_record<168, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    4,    32,   672,   882>,
        block_fft_implementation<42,   42,    4,    32,  1344,   883>
    >;
};

template<> struct block_fft_record<176, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    4,    32,   704,   884>,
        block_fft_implementation<44,   44,    4,    32,  1408,   885>,
        block_fft_implementation<22,   22,    8,    16,   704,   886>,
        block_fft_implementation<22,   22,    8,     4,  1408,   887>
    >;
};

template<> struct block_fft_record<180, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    6,    21,   720,   888>,
        block_fft_implementation<30,   30,    6,    21,  1440,   889>,
        block_fft_implementation<60,   60,    3,    10,   720,   890>,
        block_fft_implementation<60,   60,    3,     8,  1440,   891>
    >;
};

template<> struct block_fft_record<184, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    4,    32,  1472,   892>,
        block_fft_implementation<46,   46,    4,    32,   736,   893>
    >;
};

template<> struct block_fft_record<192, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    8,     4,   768,   894>,
        block_fft_implementation<24,   24,    8,     4,  1536,   895>,
        block_fft_implementation<12,   12,   16,     2,  1536,   896>,
        block_fft_implementation<12,   12,   16,     2,   768,   897>,
        block_fft_implementation<48,   48,    4,    32,   768,   898>,
        block_fft_implementation<48,   48,    4,    16,  1536,   899>,
        block_fft_implementation< 6,    6,   32,     4,  1536,   900>,
        block_fft_implementation< 6,    6,   32,     4,   768,   901>
    >;
};

template<> struct block_fft_record<200, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   10,     3,   800,   902>,
        block_fft_implementation<20,   20,   10,     3,  1600,   903>,
        block_fft_implementation<40,   40,    5,    25,   800,   904>,
        block_fft_implementation<10,   10,   20,     6,  1600,   905>,
        block_fft_implementation<40,   40,    5,    25,  1600,   906>,
        block_fft_implementation<10,   10,   20,     6,   800,   907>,
        block_fft_implementation<50,   50,    4,    32,   800,   908>,
        block_fft_implementation<50,   50,    4,    30,  1600,   909>
    >;
};

template<> struct block_fft_record<208, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    4,    32,   832,   910>,
        block_fft_implementation<52,   52,    4,    29,  1664,   911>,
        block_fft_implementation<26,   26,    8,    16,   832,   912>,
        block_fft_implementation<26,   26,    8,     4,  1664,   913>
    >;
};

template<> struct block_fft_record<224, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    8,     4,  1792,   914>,
        block_fft_implementation<56,   56,    4,    32,   896,   915>,
        block_fft_implementation<14,   14,   16,     2,  1792,   916>,
        block_fft_implementation<28,   28,    8,     4,   896,   917>,
        block_fft_implementation<56,   56,    4,    24,  1792,   918>,
        block_fft_implementation<14,   14,   16,     8,   896,   919>
    >;
};

template<> struct block_fft_record<232, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    4,    64,   928,   920>,
        block_fft_implementation<58,   58,    4,    48,  1856,   921>
    >;
};

template<> struct block_fft_record<240, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    4,    32,   960,   922>,
        block_fft_implementation<30,   30,    8,    16,   960,   923>,
        block_fft_implementation<30,   30,    8,     4,  1920,   924>,
        block_fft_implementation<60,   60,    4,    48,  1920,   925>
    >;
};

template<> struct block_fft_record<248, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    4,    64,   992,   926>,
        block_fft_implementation<62,   62,    4,    48,  1984,   927>
    >;
};

template<> struct block_fft_record<252, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    6,    21,  1008,   928>,
        block_fft_implementation<42,   42,    6,    21,  2016,   929>
    >;
};

template<> struct block_fft_record<272, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    8,    16,  2176,   930>,
        block_fft_implementation<34,   34,    8,    16,  1088,   931>
    >;
};

template<> struct block_fft_record<288, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   12,    10,  1152,   932>,
        block_fft_implementation<12,   12,   24,     5,  1152,   933>,
        block_fft_implementation<24,   24,   12,    10,  2304,   934>,
        block_fft_implementation<12,   12,   24,     5,  2304,   935>,
        block_fft_implementation<48,   48,    6,    21,  1152,   936>,
        block_fft_implementation<36,   36,    8,     4,  2304,   937>,
        block_fft_implementation<18,   18,   16,     2,  2304,   938>,
        block_fft_implementation< 6,    6,   48,     4,  2304,   939>,
        block_fft_implementation<36,   36,    8,    16,  1152,   940>,
        block_fft_implementation<48,   48,    6,    21,  2304,   941>,
        block_fft_implementation< 6,    6,   48,     2,  1152,   942>,
        block_fft_implementation<18,   18,   16,     4,  1152,   943>
    >;
};

template<> struct block_fft_record<300, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   10,    12,  1200,   944>,
        block_fft_implementation<30,   30,   10,     3,  2400,   945>,
        block_fft_implementation<60,   60,    5,    25,  1200,   946>,
        block_fft_implementation<60,   60,    5,    19,  2400,   947>
    >;
};

template<> struct block_fft_record<304, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    8,    16,  2432,   948>,
        block_fft_implementation<38,   38,    8,    16,  1216,   949>
    >;
};

template<> struct block_fft_record<320, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    8,    16,  1280,   950>,
        block_fft_implementation<20,   20,   16,     2,  2560,   951>,
        block_fft_implementation<20,   20,   16,     2,  1280,   952>,
        block_fft_implementation<40,   40,    8,    16,  2560,   953>,
        block_fft_implementation<10,   10,   32,     2,  2560,   954>,
        block_fft_implementation<10,   10,   32,     4,  1280,   955>
    >;
};

template<> struct block_fft_record<336, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    8,    16,  2688,   956>,
        block_fft_implementation<42,   42,    8,    16,  1344,   957>
    >;
};

template<> struct block_fft_record<352, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    8,    16,  2816,   958>,
        block_fft_implementation<22,   22,   16,     8,  2816,   959>,
        block_fft_implementation<44,   44,    8,    16,  1408,   960>,
        block_fft_implementation<22,   22,   16,     8,  1408,   961>
    >;
};

template<> struct block_fft_record<360, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    6,    21,  1440,   962>,
        block_fft_implementation<30,   30,   12,    10,  1440,   963>,
        block_fft_implementation<30,   30,   12,    10,  2880,   964>,
        block_fft_implementation<60,   60,    6,     4,  2880,   965>
    >;
};

template<> struct block_fft_record<368, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    8,    16,  2944,   966>,
        block_fft_implementation<46,   46,    8,    16,  1472,   967>
    >;
};

template<> struct block_fft_record<384, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,   32,     1,  1536,   968>,
        block_fft_implementation<48,   48,    8,    16,  1536,   969>,
        block_fft_implementation<24,   24,   16,     8,  1536,   970>,
        block_fft_implementation<12,   12,   32,     1,  3072,   971>,
        block_fft_implementation<24,   24,   16,     2,  3072,   972>,
        block_fft_implementation<48,   48,    8,    16,  3072,   973>,
        block_fft_implementation< 6,    6,   64,     2,  3072,   974>,
        block_fft_implementation< 6,    6,   64,     2,  1536,   975>
    >;
};

template<> struct block_fft_record<392, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   14,     9,  1568,   976>,
        block_fft_implementation<28,   28,   14,     9,  3136,   977>,
        block_fft_implementation<56,   56,    7,    18,  1568,   978>,
        block_fft_implementation<14,   14,   28,     1,  1568,   979>,
        block_fft_implementation<14,   14,   28,     1,  3136,   980>,
        block_fft_implementation<56,   56,    7,    31,  3136,   981>
    >;
};

template<> struct block_fft_record<416, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   16,     8,  3328,   982>,
        block_fft_implementation<52,   52,    8,    28,  3328,   983>,
        block_fft_implementation<52,   52,    8,    16,  1664,   984>,
        block_fft_implementation<26,   26,   16,     8,  1664,   985>
    >;
};

template<> struct block_fft_record<432, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,   12,    10,  1728,   986>,
        block_fft_implementation<36,   36,   12,    10,  3456,   987>,
        block_fft_implementation<12,   12,   36,     7,  1728,   988>,
        block_fft_implementation<24,   24,   18,     7,  1728,   989>,
        block_fft_implementation<12,   12,   36,     7,  3456,   990>,
        block_fft_implementation< 6,    6,   72,     3,  1728,   991>,
        block_fft_implementation< 6,    6,   72,     3,  3456,   992>,
        block_fft_implementation<24,   24,   18,     7,  3456,   993>,
        block_fft_implementation<18,   18,   24,     5,  3456,   994>,
        block_fft_implementation<18,   18,   24,     5,  1728,   995>,
        block_fft_implementation<48,   48,    9,    14,  1728,   996>,
        block_fft_implementation<54,   54,    8,    16,  1728,   997>,
        block_fft_implementation<48,   48,    9,    14,  3456,   998>,
        block_fft_implementation<54,   54,    8,    28,  3456,   999>
    >;
};

template<> struct block_fft_record<448, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   16,     8,  3584,  1000>,
        block_fft_implementation<56,   56,    8,    16,  1792,  1001>,
        block_fft_implementation<28,   28,   16,     8,  1792,  1002>,
        block_fft_implementation<56,   56,    8,    27,  3584,  1003>,
        block_fft_implementation<14,   14,   32,     1,  3584,  1004>,
        block_fft_implementation<14,   14,   32,     4,  1792,  1005>
    >;
};

template<> struct block_fft_record<464, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    8,    16,  1856,  1006>,
        block_fft_implementation<58,   58,    8,    24,  3712,  1007>
    >;
};

template<> struct block_fft_record<480, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   16,     8,  3840,  1008>,
        block_fft_implementation<60,   60,    8,    16,  1920,  1009>,
        block_fft_implementation<30,   30,   16,     8,  1920,  1010>,
        block_fft_implementation<60,   60,    8,    24,  3840,  1011>
    >;
};

template<> struct block_fft_record<496, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    8,    32,  1984,  1012>,
        block_fft_implementation<62,   62,    8,    24,  3968,  1013>
    >;
};

template<> struct block_fft_record<500, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   25,     5,  2000,  1014>,
        block_fft_implementation<50,   50,   10,    25,  2000,  1015>,
        block_fft_implementation<10,   10,   50,     5,  2000,  1016>,
        block_fft_implementation<50,   50,   10,    24,  4000,  1017>,
        block_fft_implementation<20,   20,   25,     5,  4000,  1018>,
        block_fft_implementation<10,   10,   50,     5,  4000,  1019>
    >;
};

template<> struct block_fft_record<504, float, fft_type::c2c, fft_direction::inverse, 700> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,   12,    10,  4032,  1020>,
        block_fft_implementation<42,   42,   12,    16,  2016,  1021>
    >;
};
