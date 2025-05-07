//Copyright (c) 2019-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
//NVIDIA CORPORATION and its licensors retain all intellectual property
//and proprietary rights in and to this software, related documentation
//and any modifications thereto.  Any use, reproduction, disclosure or
//distribution of this software and related documentation without an express
//license agreement from NVIDIA CORPORATION is strictly prohibited.
//


template<> struct block_fft_record<33, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<33,   33,    1,    64,     0,  2461>
    >;
};

template<> struct block_fft_record<34, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    1,    64,     0,  2462>
    >;
};

template<> struct block_fft_record<35, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<35,   35,    1,    64,     0,  2463>
    >;
};

template<> struct block_fft_record<37, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<37,   37,    1,    64,     0,  2464>
    >;
};

template<> struct block_fft_record<38, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    1,    64,     0,  2465>
    >;
};

template<> struct block_fft_record<39, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<39,   39,    1,    64,     0,  2466>
    >;
};

template<> struct block_fft_record<40, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    2,   384,    80,  2467>,
        block_fft_implementation<20,   20,    2,   640,   160,  2468>,
        block_fft_implementation<10,   10,    4,   128,   160,  2469>,
        block_fft_implementation<40,   40,    1,    32,     0,  2470>
    >;
};

template<> struct block_fft_record<41, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<41,   41,    1,    64,     0,  2471>
    >;
};

template<> struct block_fft_record<42, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    1,    64,     0,  2472>
    >;
};

template<> struct block_fft_record<43, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<43,   43,    1,    64,     0,  2473>
    >;
};

template<> struct block_fft_record<44, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    1,    64,     0,  2474>
    >;
};

template<> struct block_fft_record<45, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<45,   45,    1,    64,     0,  2475>
    >;
};

template<> struct block_fft_record<46, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    1,    64,     0,  2476>
    >;
};

template<> struct block_fft_record<47, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<47,   47,    1,    64,     0,  2477>
    >;
};

template<> struct block_fft_record<48, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<48,   48,    1,    64,     0,  2478>
    >;
};

template<> struct block_fft_record<50, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<50,   50,    1,    64,     0,  2479>
    >;
};

template<> struct block_fft_record<51, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<51,   51,    1,    64,     0,  2480>
    >;
};

template<> struct block_fft_record<52, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    1,    64,     0,  2481>
    >;
};

template<> struct block_fft_record<53, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<53,   53,    1,    64,     0,  2482>
    >;
};

template<> struct block_fft_record<54, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<54,   54,    1,    64,     0,  2483>
    >;
};

template<> struct block_fft_record<55, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<55,   55,    1,    64,     0,  2484>
    >;
};

template<> struct block_fft_record<56, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    1,    64,     0,  2485>
    >;
};

template<> struct block_fft_record<57, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<57,   57,    1,    64,     0,  2486>
    >;
};

template<> struct block_fft_record<58, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    1,    64,     0,  2487>
    >;
};

template<> struct block_fft_record<59, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<59,   59,    1,    64,     0,  2488>
    >;
};

template<> struct block_fft_record<60, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    1,    64,     0,  2489>
    >;
};

template<> struct block_fft_record<61, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<61,   61,    1,    64,     0,  2490>
    >;
};

template<> struct block_fft_record<62, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    1,    64,     0,  2491>
    >;
};

template<> struct block_fft_record<63, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<63,   63,    1,    64,     0,  2492>
    >;
};

template<> struct block_fft_record<2, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 2,    2,    1,  1024,     0,  2493>
    >;
};

template<> struct block_fft_record<4, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4,    1,  1024,     0,  2494>,
        block_fft_implementation< 2,    2,    2,   384,     8,  2495>,
        block_fft_implementation< 2,    2,    2,   224,    16,  2496>
    >;
};

template<> struct block_fft_record<8, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    1,   448,     0,  2497>,
        block_fft_implementation< 4,    4,    2,   768,    16,  2498>,
        block_fft_implementation< 4,    4,    2,   224,    32,  2499>,
        block_fft_implementation< 2,    2,    4,   128,    16,  2500>,
        block_fft_implementation< 2,    2,    4,   128,    32,  2501>
    >;
};

template<> struct block_fft_record<16, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    1,   896,     0,  2502>,
        block_fft_implementation< 4,    4,    4,   384,    32,  2503>,
        block_fft_implementation< 4,    4,    4,   128,    64,  2504>,
        block_fft_implementation< 8,    8,    2,   544,    32,  2505>,
        block_fft_implementation< 8,    8,    2,   160,    64,  2506>,
        block_fft_implementation< 2,    2,    8,   128,    32,  2507>,
        block_fft_implementation< 2,    2,    8,    64,    64,  2508>
    >;
};

template<> struct block_fft_record<32, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,    1,  1024,     0,  2509>,
        block_fft_implementation< 8,    8,    4,    58,   128,  2510>,
        block_fft_implementation< 8,    8,    4,   320,    64,  2511>,
        block_fft_implementation< 4,    4,    8,    56,   128,  2512>,
        block_fft_implementation< 4,    4,    8,    62,    64,  2513>,
        block_fft_implementation<16,   16,    2,    28,   128,  2515>,
        block_fft_implementation< 2,    2,   16,    32,   128,  2514>,
        block_fft_implementation< 2,    2,   16,    64,    64,  2516>,
        block_fft_implementation<16,   16,    2,    96,    64,  2517>
    >;
};

template<> struct block_fft_record<64, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    8,   128,   128,  2519>,
        block_fft_implementation< 8,    8,    8,    16,   256,  2518>,
        block_fft_implementation< 4,    4,   16,    16,   256,  2520>,
        block_fft_implementation< 4,    4,   16,    60,   128,  2521>,
        block_fft_implementation<16,   16,    4,    16,   256,  2522>,
        block_fft_implementation<16,   16,    4,    42,   128,  2523>,
        block_fft_implementation<32,   32,    2,    30,   256,  2524>,
        block_fft_implementation< 2,    2,   32,    32,   128,  2526>,
        block_fft_implementation< 2,    2,   32,    20,   256,  2525>,
        block_fft_implementation<32,   32,    2,    32,   128,  2527>,
        block_fft_implementation<64,   64,    1,   512,     0,  2528>
    >;
};

template<> struct block_fft_record<128, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    8,    16,   256,  2529>,
        block_fft_implementation< 8,    8,   16,    16,   512,  2530>,
        block_fft_implementation<16,   16,    8,     8,   512,  2531>,
        block_fft_implementation< 8,    8,   16,    16,   256,  2532>,
        block_fft_implementation< 4,    4,   32,    16,   512,  2533>,
        block_fft_implementation< 4,    4,   32,    16,   256,  2534>,
        block_fft_implementation<32,   32,    4,    16,   512,  2535>,
        block_fft_implementation<32,   32,    4,    16,   256,  2536>,
        block_fft_implementation< 2,    2,   64,    10,   256,  2538>,
        block_fft_implementation< 2,    2,   64,    10,   512,  2537>
    >;
};

template<> struct block_fft_record<256, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,   16,     8,   512,  2539>,
        block_fft_implementation< 8,    8,   32,     8,  1024,  2540>,
        block_fft_implementation< 8,    8,   32,     8,   512,  2541>,
        block_fft_implementation<16,   16,   16,     4,  1024,  2542>,
        block_fft_implementation< 4,    4,   64,     8,  1024,  2544>,
        block_fft_implementation<32,   32,    8,     8,  1024,  2543>,
        block_fft_implementation< 4,    4,   64,     8,   512,  2545>,
        block_fft_implementation<32,   32,    8,     8,   512,  2546>,
        block_fft_implementation< 2,    2,  128,     4,   512,  2548>,
        block_fft_implementation< 2,    2,  128,     8,  1024,  2547>
    >;
};

template<> struct block_fft_record<512, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,   64,     4,  2048,  2549>,
        block_fft_implementation< 8,    8,   64,     4,  1024,  2550>,
        block_fft_implementation<16,   16,   32,     4,  1024,  2551>,
        block_fft_implementation<32,   32,   16,     4,  2048,  2552>,
        block_fft_implementation<32,   32,   16,     4,  1024,  2553>,
        block_fft_implementation<16,   16,   32,     2,  2048,  2554>,
        block_fft_implementation< 4,    4,  128,     4,  2048,  2555>,
        block_fft_implementation< 4,    4,  128,     4,  1024,  2556>,
        block_fft_implementation< 2,    2,  256,     2,  1024,  2558>,
        block_fft_implementation< 2,    2,  256,     4,  2048,  2557>
    >;
};

template<> struct block_fft_record<1024, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,   64,     2,  2048,  2559>,
        block_fft_implementation<32,   32,   32,     4,  2048,  2563>,
        block_fft_implementation< 8,    8,  128,     2,  4096,  2560>,
        block_fft_implementation<32,   32,   32,     2,  4096,  2561>,
        block_fft_implementation< 8,    8,  128,     2,  2048,  2562>,
        block_fft_implementation<16,   16,   64,     2,  4096,  2564>,
        block_fft_implementation< 4,    4,  256,     2,  4096,  2565>,
        block_fft_implementation< 4,    4,  256,     2,  2048,  2566>,
        block_fft_implementation< 2,    2,  512,     2,  2048,  2568>,
        block_fft_implementation< 2,    2,  512,     4,  4096,  2567>
    >;
};

template<> struct block_fft_record<2048, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  128,     2,  4096,  2569>,
        block_fft_implementation< 8,    8,  256,     2,  8192,  2570>,
        block_fft_implementation< 8,    8,  256,     2,  4096,  2571>,
        block_fft_implementation<32,   32,   64,     2,  4096,  2574>,
        block_fft_implementation<16,   16,  128,     2,  8192,  2572>,
        block_fft_implementation<32,   32,   64,     2,  8192,  2573>,
        block_fft_implementation< 4,    4,  512,     2,  8192,  2575>,
        block_fft_implementation< 4,    4,  512,     2,  4096,  2576>,
        block_fft_implementation< 2,    2, 1024,     2,  4096,  2578>,
        block_fft_implementation< 2,    2, 1024,     2,  8192,  2577>
    >;
};

template<> struct block_fft_record<4096, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  256,     2,  8192,  2579>,
        block_fft_implementation< 8,    8,  512,     2, 16384,  2580>,
        block_fft_implementation< 8,    8,  512,     2,  8192,  2581>,
        block_fft_implementation<32,   32,  128,     2,  8192,  2584>,
        block_fft_implementation<16,   16,  256,     2, 16384,  2582>,
        block_fft_implementation<32,   32,  128,     2, 16384,  2583>,
        block_fft_implementation< 4,    4, 1024,     2, 16384,  2585>,
        block_fft_implementation< 4,    4, 1024,     2,  8192,  2586>
    >;
};

template<> struct block_fft_record<8192, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  512,     2, 16384,  2587>,
        block_fft_implementation< 8,    8, 1024,     2, 32768,  2590>,
        block_fft_implementation<32,   32,  256,     2, 32768,  2588>,
        block_fft_implementation<32,   32,  256,     2, 16384,  2589>,
        block_fft_implementation< 8,    8, 1024,     2, 16384,  2592>,
        block_fft_implementation<16,   16,  512,     2, 32768,  2591>
    >;
};

template<> struct block_fft_record<16384, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16, 1024,     2, 32768,  2593>,
        block_fft_implementation<32,   32,  512,     2, 32768,  2594>
    >;
};

template<> struct block_fft_record<3, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,    1,  1024,     0,  2595>
    >;
};

template<> struct block_fft_record<9, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    1,   768,     0,  2596>,
        block_fft_implementation< 3,    3,    3,   256,    36,  2597>,
        block_fft_implementation< 3,    3,    3,   128,    18,  2598>
    >;
};

template<> struct block_fft_record<27, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    1,  1024,     0,  2599>,
        block_fft_implementation< 9,    9,    3,   256,   108,  2601>,
        block_fft_implementation< 9,    9,    3,   128,    54,  2600>,
        block_fft_implementation< 3,    3,    9,   224,   108,  2602>,
        block_fft_implementation< 3,    3,    9,    64,    54,  2603>
    >;
};

template<> struct block_fft_record<81, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    9,    14,   162,  2605>,
        block_fft_implementation< 9,    9,    9,    28,   324,  2604>,
        block_fft_implementation<27,   27,    3,    42,   162,  2606>,
        block_fft_implementation<27,   27,    3,    42,   324,  2607>,
        block_fft_implementation< 3,    3,   27,    32,   324,  2608>,
        block_fft_implementation< 3,    3,   27,    28,   162,  2609>
    >;
};

template<> struct block_fft_record<243, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    9,    14,   972,  2610>,
        block_fft_implementation<27,   27,    9,    14,   486,  2611>,
        block_fft_implementation< 9,    9,   27,    16,   972,  2612>,
        block_fft_implementation< 9,    9,   27,    18,   486,  2613>,
        block_fft_implementation< 3,    3,   81,    12,   972,  2614>,
        block_fft_implementation< 3,    3,   81,     6,   486,  2615>
    >;
};

template<> struct block_fft_record<729, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,   27,    18,  2916,  2616>,
        block_fft_implementation<27,   27,   27,    18,  1458,  2617>,
        block_fft_implementation< 9,    9,   81,     6,  2916,  2618>,
        block_fft_implementation< 9,    9,   81,     6,  1458,  2619>,
        block_fft_implementation< 3,    3,  243,     4,  2916,  2620>,
        block_fft_implementation< 3,    3,  243,     2,  1458,  2621>
    >;
};

template<> struct block_fft_record<2187, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,   81,     6,  8748,  2623>,
        block_fft_implementation<27,   27,   81,     6,  4374,  2625>,
        block_fft_implementation< 9,    9,  243,     2,  8748,  2622>,
        block_fft_implementation< 9,    9,  243,     2,  4374,  2624>,
        block_fft_implementation< 3,    3,  729,     2,  8748,  2626>,
        block_fft_implementation< 3,    3,  729,     2,  4374,  2627>
    >;
};

template<> struct block_fft_record<6561, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,  243,     2, 26244,  2629>,
        block_fft_implementation<27,   27,  243,     2, 13122,  2628>,
        block_fft_implementation< 9,    9,  729,     2, 26244,  2631>,
        block_fft_implementation< 9,    9,  729,     2, 13122,  2630>
    >;
};

template<> struct block_fft_record<5, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,    1,   896,     0,  2633>
    >;
};

template<> struct block_fft_record<25, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    1,  1024,     0,  2634>,
        block_fft_implementation< 5,    5,    5,   256,   100,  2635>,
        block_fft_implementation< 5,    5,    5,    38,    50,  2636>
    >;
};

template<> struct block_fft_record<125, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    5,    24,   250,  2637>,
        block_fft_implementation<25,   25,    5,    50,   500,  2638>,
        block_fft_implementation< 5,    5,   25,    20,   500,  2639>,
        block_fft_implementation< 5,    5,   25,    20,   250,  2640>
    >;
};

template<> struct block_fft_record<625, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,   25,    10,  2500,  2642>,
        block_fft_implementation<25,   25,   25,    20,  1250,  2641>,
        block_fft_implementation< 5,    5,  125,     2,  2500,  2643>,
        block_fft_implementation< 5,    5,  125,     4,  1250,  2644>
    >;
};

template<> struct block_fft_record<3125, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,  125,     4, 12500,  2646>,
        block_fft_implementation<25,   25,  125,     2,  6250,  2645>,
        block_fft_implementation< 5,    5,  625,     2, 12500,  2647>,
        block_fft_implementation< 5,    5,  625,     2,  6250,  2648>
    >;
};

template<> struct block_fft_record<15625, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,  625,     2, 31250,  2649>
    >;
};

template<> struct block_fft_record<7, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    1,  1024,     0,  2650>
    >;
};

template<> struct block_fft_record<49, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    7,    64,   196,  2652>,
        block_fft_implementation< 7,    7,    7,    64,    98,  2653>,
        block_fft_implementation<49,   49,    1,   512,     0,  2651>
    >;
};

template<> struct block_fft_record<343, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,   49,    10,  1372,  2654>,
        block_fft_implementation< 7,    7,   49,    10,   686,  2655>
    >;
};

template<> struct block_fft_record<2401, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,  343,     2,  9604,  2656>,
        block_fft_implementation< 7,    7,  343,     2,  4802,  2657>
    >;
};

template<> struct block_fft_record<11, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,    1,   896,     0,  2659>
    >;
};

template<> struct block_fft_record<121, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,   11,    46,   484,  2660>,
        block_fft_implementation<11,   11,   11,    22,   242,  2661>
    >;
};

template<> struct block_fft_record<1331, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,  121,     2,  5324,  2663>,
        block_fft_implementation<11,   11,  121,     2,  2662,  2662>
    >;
};

template<> struct block_fft_record<6, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    1,  1024,     0,  2664>
    >;
};

template<> struct block_fft_record<36, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    6,   128,   144,  2666>,
        block_fft_implementation< 6,    6,    6,   160,    72,  2665>,
        block_fft_implementation<36,   36,    1,  1024,     0,  2667>
    >;
};

template<> struct block_fft_record<216, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,   36,    10,   864,  2668>,
        block_fft_implementation< 6,    6,   36,    28,   432,  2669>
    >;
};

template<> struct block_fft_record<1296, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,   36,     6,  2592,  2670>,
        block_fft_implementation<36,   36,   36,     6,  5184,  2671>,
        block_fft_implementation< 6,    6,  216,     2,  5184,  2672>,
        block_fft_implementation< 6,    6,  216,     2,  2592,  2673>
    >;
};

template<> struct block_fft_record<7776, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,  216,     2, 31104,  2674>,
        block_fft_implementation<36,   36,  216,     2, 15552,  2675>
    >;
};

template<> struct block_fft_record<10, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,    1,   768,     0,  2676>
    >;
};

template<> struct block_fft_record<100, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,   10,    12,   400,  2678>,
        block_fft_implementation<10,   10,   10,    48,   200,  2677>
    >;
};

template<> struct block_fft_record<1000, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,  100,     2,  4000,  2679>,
        block_fft_implementation<10,   10,  100,     2,  2000,  2680>
    >;
};

template<> struct block_fft_record<10000, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10, 1000,     2, 20000,  2682>
    >;
};

template<> struct block_fft_record<12, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    1,   896,     0,  2683>
    >;
};

template<> struct block_fft_record<144, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,   12,    20,   288,  2685>,
        block_fft_implementation<12,   12,   12,    10,   576,  2684>
    >;
};

template<> struct block_fft_record<1728, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,  144,     4,  3456,  2687>,
        block_fft_implementation<12,   12,  144,     4,  6912,  2686>
    >;
};

template<> struct block_fft_record<13, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,    1,   768,     0,  2688>
    >;
};

template<> struct block_fft_record<169, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,   13,    38,   676,  2689>,
        block_fft_implementation<13,   13,   13,    18,   338,  2690>
    >;
};

template<> struct block_fft_record<2197, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,  169,     6,  8788,  2692>,
        block_fft_implementation<13,   13,  169,     4,  4394,  2691>
    >;
};

template<> struct block_fft_record<14, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,    1,   896,     0,  2693>
    >;
};

template<> struct block_fft_record<196, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,   14,    36,   784,  2694>,
        block_fft_implementation<14,   14,   14,    18,   392,  2695>
    >;
};

template<> struct block_fft_record<2744, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,  196,     2, 10976,  2696>,
        block_fft_implementation<14,   14,  196,     2,  5488,  2697>
    >;
};

template<> struct block_fft_record<15, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,    1,   512,     0,  2698>
    >;
};

template<> struct block_fft_record<225, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,   15,    34,   900,  2699>,
        block_fft_implementation<15,   15,   15,     4,   450,  2700>
    >;
};

template<> struct block_fft_record<3375, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,  225,     2, 13500,  2701>,
        block_fft_implementation<15,   15,  225,     2,  6750,  2702>
    >;
};

template<> struct block_fft_record<17, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,    1,  1024,     0,  2703>
    >;
};

template<> struct block_fft_record<289, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,   17,    14,  1156,  2704>,
        block_fft_implementation<17,   17,   17,    14,   578,  2705>
    >;
};

template<> struct block_fft_record<4913, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,  289,     4,  9826,  2707>,
        block_fft_implementation<17,   17,  289,     2, 19652,  2706>
    >;
};

template<> struct block_fft_record<18, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    1,  1024,     0,  2708>
    >;
};

template<> struct block_fft_record<324, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,   18,    14,   648,  2710>,
        block_fft_implementation<18,   18,   18,    14,  1296,  2709>
    >;
};

template<> struct block_fft_record<5832, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,  324,     2, 23328,  2711>,
        block_fft_implementation<18,   18,  324,     2, 11664,  2712>
    >;
};

template<> struct block_fft_record<19, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,    1,  1024,     0,  2713>
    >;
};

template<> struct block_fft_record<361, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,   19,    40,  1444,  2714>,
        block_fft_implementation<19,   19,   19,     6,   722,  2715>
    >;
};

template<> struct block_fft_record<6859, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,  361,     2, 27436,  2716>,
        block_fft_implementation<19,   19,  361,     2, 13718,  2717>
    >;
};

template<> struct block_fft_record<20, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    1,  1024,     0,  2718>
    >;
};

template<> struct block_fft_record<400, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   20,    38,   800,  2720>,
        block_fft_implementation<20,   20,   20,     6,  1600,  2719>
    >;
};

template<> struct block_fft_record<8000, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,  400,     2, 32000,  2722>,
        block_fft_implementation<20,   20,  400,     2, 16000,  2721>
    >;
};

template<> struct block_fft_record<21, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,    1,  1024,     0,  2723>
    >;
};

template<> struct block_fft_record<441, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,   21,    12,   882,  2725>,
        block_fft_implementation<21,   21,   21,     6,  1764,  2724>
    >;
};

template<> struct block_fft_record<9261, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,  441,     2, 18522,  2726>
    >;
};

template<> struct block_fft_record<22, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    1,  1024,     0,  2728>
    >;
};

template<> struct block_fft_record<484, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,   22,    22,   968,  2730>,
        block_fft_implementation<22,   22,   22,    10,  1936,  2729>
    >;
};

template<> struct block_fft_record<10648, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,  484,     2, 21296,  2732>
    >;
};

template<> struct block_fft_record<23, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,    1,  1024,     0,  2733>
    >;
};

template<> struct block_fft_record<529, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,   23,    22,  2116,  2734>,
        block_fft_implementation<23,   23,   23,    22,  1058,  2735>
    >;
};

template<> struct block_fft_record<12167, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,  529,     2, 24334,  2737>
    >;
};

template<> struct block_fft_record<24, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    1,  1024,     0,  2738>
    >;
};

template<> struct block_fft_record<576, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   24,    10,  1152,  2739>,
        block_fft_implementation<24,   24,   24,    10,  2304,  2740>
    >;
};

template<> struct block_fft_record<13824, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,  576,     2, 27648,  2741>
    >;
};

template<> struct block_fft_record<26, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    1,  1024,     0,  2742>
    >;
};

template<> struct block_fft_record<676, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   26,    18,  1352,  2744>,
        block_fft_implementation<26,   26,   26,    18,  2704,  2743>
    >;
};

template<> struct block_fft_record<28, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    1,  1024,     0,  2746>
    >;
};

template<> struct block_fft_record<784, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   28,    18,  1568,  2747>,
        block_fft_implementation<28,   28,   28,     2,  3136,  2748>
    >;
};

template<> struct block_fft_record<29, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,    1,  1024,     0,  2750>
    >;
};

template<> struct block_fft_record<841, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,   29,    26,  1682,  2752>,
        block_fft_implementation<29,   29,   29,    16,  3364,  2751>
    >;
};

template<> struct block_fft_record<30, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    1,  1024,     0,  2754>
    >;
};

template<> struct block_fft_record<900, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   30,     8,  1800,  2756>,
        block_fft_implementation<30,   30,   30,     2,  3600,  2755>
    >;
};

template<> struct block_fft_record<31, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,    1,  1024,     0,  2757>
    >;
};

template<> struct block_fft_record<961, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,   31,    16,  3844,  2758>,
        block_fft_implementation<31,   31,   31,     2,  1922,  2759>
    >;
};

template<> struct block_fft_record<68, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    2,    32,   136,  2760>,
        block_fft_implementation<34,   34,    2,    32,   272,  2761>
    >;
};

template<> struct block_fft_record<72, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    6,    20,   144,  2762>,
        block_fft_implementation<12,   12,    6,    20,   288,  2763>,
        block_fft_implementation<36,   36,    2,   256,   144,  2765>,
        block_fft_implementation<24,   24,    3,    64,   144,  2764>,
        block_fft_implementation<36,   36,    2,   224,   288,  2771>,
        block_fft_implementation<24,   24,    3,    36,   288,  2766>,
        block_fft_implementation<18,   18,    4,    32,   144,  2768>,
        block_fft_implementation<18,   18,    4,    56,   288,  2769>,
        block_fft_implementation< 6,    6,   12,    32,   288,  2767>,
        block_fft_implementation< 6,    6,   12,    32,   144,  2770>
    >;
};

template<> struct block_fft_record<76, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    2,    64,   152,  2772>,
        block_fft_implementation<38,   38,    2,    30,   304,  2773>
    >;
};

template<> struct block_fft_record<80, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    4,   320,   160,  2774>,
        block_fft_implementation<20,   20,    4,   192,   320,  2775>,
        block_fft_implementation<40,   40,    2,   320,   160,  2776>,
        block_fft_implementation<40,   40,    2,   160,   320,  2779>,
        block_fft_implementation<10,   10,    8,    64,   320,  2777>,
        block_fft_implementation<10,   10,    8,    96,   160,  2778>
    >;
};

template<> struct block_fft_record<84, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    2,   384,   168,  2780>,
        block_fft_implementation<42,   42,    2,    32,   336,  2781>
    >;
};

template<> struct block_fft_record<88, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    2,    32,   176,  2782>,
        block_fft_implementation<44,   44,    2,    64,   352,  2785>,
        block_fft_implementation<22,   22,    4,    16,   352,  2784>,
        block_fft_implementation<22,   22,    4,    64,   176,  2783>
    >;
};

template<> struct block_fft_record<92, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    2,    32,   184,  2786>,
        block_fft_implementation<46,   46,    2,   128,   368,  2787>
    >;
};

template<> struct block_fft_record<96, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    4,    16,   384,  2788>,
        block_fft_implementation<12,   12,    8,     8,   384,  2789>,
        block_fft_implementation<24,   24,    4,   256,   192,  2790>,
        block_fft_implementation< 6,    6,   16,    16,   384,  2791>,
        block_fft_implementation<12,   12,    8,    24,   192,  2792>,
        block_fft_implementation<48,   48,    2,    60,   384,  2794>,
        block_fft_implementation< 6,    6,   16,    22,   192,  2793>,
        block_fft_implementation<48,   48,    2,   192,   192,  2795>
    >;
};

template<> struct block_fft_record<104, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    2,    64,   208,  2796>,
        block_fft_implementation<52,   52,    2,    32,   416,  2799>,
        block_fft_implementation<26,   26,    4,    32,   416,  2798>,
        block_fft_implementation<26,   26,    4,    64,   208,  2797>
    >;
};

template<> struct block_fft_record<108, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    6,    42,   216,  2801>,
        block_fft_implementation<18,   18,    6,    42,   432,  2800>,
        block_fft_implementation<36,   36,    3,    42,   216,  2802>,
        block_fft_implementation<54,   54,    2,    64,   216,  2803>,
        block_fft_implementation<36,   36,    3,    18,   432,  2806>,
        block_fft_implementation<54,   54,    2,   128,   432,  2809>,
        block_fft_implementation< 6,    6,   18,    24,   432,  2804>,
        block_fft_implementation<12,   12,    9,    20,   216,  2807>,
        block_fft_implementation< 6,    6,   18,    54,   216,  2805>,
        block_fft_implementation<12,   12,    9,    56,   432,  2808>
    >;
};

template<> struct block_fft_record<112, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    4,    16,   224,  2810>,
        block_fft_implementation<28,   28,    4,    32,   448,  2811>,
        block_fft_implementation<56,   56,    2,   256,   224,  2812>,
        block_fft_implementation<56,   56,    2,    62,   448,  2815>,
        block_fft_implementation<14,   14,    8,     8,   448,  2813>,
        block_fft_implementation<14,   14,    8,    32,   224,  2814>
    >;
};

template<> struct block_fft_record<116, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    2,    32,   232,  2816>,
        block_fft_implementation<58,   58,    2,   128,   464,  2817>
    >;
};

template<> struct block_fft_record<120, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    2,   224,   240,  2818>,
        block_fft_implementation<60,   60,    2,    32,   480,  2821>,
        block_fft_implementation<30,   30,    4,    32,   480,  2820>,
        block_fft_implementation<30,   30,    4,    32,   240,  2819>
    >;
};

template<> struct block_fft_record<124, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    2,    64,   248,  2822>,
        block_fft_implementation<62,   62,    2,    32,   496,  2823>
    >;
};

template<> struct block_fft_record<136, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    4,    48,   272,  2824>,
        block_fft_implementation<34,   34,    4,    16,   544,  2825>
    >;
};

template<> struct block_fft_record<152, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    4,    16,   304,  2827>,
        block_fft_implementation<38,   38,    4,    16,   608,  2826>
    >;
};

template<> struct block_fft_record<160, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    4,    16,   640,  2830>,
        block_fft_implementation<20,   20,    8,     8,   640,  2828>,
        block_fft_implementation<40,   40,    4,   192,   320,  2829>,
        block_fft_implementation<10,   10,   16,    16,   640,  2831>,
        block_fft_implementation<20,   20,    8,    96,   320,  2832>,
        block_fft_implementation<10,   10,   16,    32,   320,  2833>
    >;
};

template<> struct block_fft_record<168, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    4,    16,   336,  2834>,
        block_fft_implementation<42,   42,    4,    16,   672,  2835>
    >;
};

template<> struct block_fft_record<176, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    4,    16,   352,  2836>,
        block_fft_implementation<44,   44,    4,    30,   704,  2837>,
        block_fft_implementation<22,   22,    8,     8,   704,  2838>,
        block_fft_implementation<22,   22,    8,    32,   352,  2839>
    >;
};

template<> struct block_fft_record<180, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    6,    42,   360,  2840>,
        block_fft_implementation<30,   30,    6,    10,   720,  2841>,
        block_fft_implementation<60,   60,    3,    20,   360,  2842>,
        block_fft_implementation<60,   60,    3,    42,   720,  2843>
    >;
};

template<> struct block_fft_record<184, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    4,    64,   368,  2845>,
        block_fft_implementation<46,   46,    4,    32,   736,  2844>
    >;
};

template<> struct block_fft_record<192, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    8,     8,   384,  2846>,
        block_fft_implementation<24,   24,    8,     8,   768,  2847>,
        block_fft_implementation<12,   12,   16,     8,   768,  2848>,
        block_fft_implementation<12,   12,   16,    12,   384,  2849>,
        block_fft_implementation<48,   48,    4,    14,   384,  2850>,
        block_fft_implementation<48,   48,    4,    14,   768,  2852>,
        block_fft_implementation< 6,    6,   32,     8,   768,  2851>,
        block_fft_implementation< 6,    6,   32,    16,   384,  2853>
    >;
};

template<> struct block_fft_record<200, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   10,    12,   400,  2855>,
        block_fft_implementation<20,   20,   10,    12,   800,  2854>,
        block_fft_implementation<40,   40,    5,    50,   400,  2856>,
        block_fft_implementation<10,   10,   20,    12,   800,  2857>,
        block_fft_implementation<40,   40,    5,    40,   800,  2859>,
        block_fft_implementation<50,   50,    4,    16,   400,  2860>,
        block_fft_implementation<10,   10,   20,    22,   400,  2858>,
        block_fft_implementation<50,   50,    4,    64,   800,  2861>
    >;
};

template<> struct block_fft_record<208, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    4,    32,   416,  2862>,
        block_fft_implementation<52,   52,    4,    16,   832,  2863>,
        block_fft_implementation<26,   26,    8,    16,   832,  2864>,
        block_fft_implementation<26,   26,    8,    16,   416,  2865>
    >;
};

template<> struct block_fft_record<224, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    8,    16,   896,  2866>,
        block_fft_implementation<56,   56,    4,    96,   448,  2867>,
        block_fft_implementation<56,   56,    4,    16,   896,  2869>,
        block_fft_implementation<14,   14,   16,     8,   896,  2868>,
        block_fft_implementation<28,   28,    8,   128,   448,  2870>,
        block_fft_implementation<14,   14,   16,    24,   448,  2871>
    >;
};

template<> struct block_fft_record<232, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    4,    16,   464,  2872>,
        block_fft_implementation<58,   58,    4,    34,   928,  2873>
    >;
};

template<> struct block_fft_record<240, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    4,    16,   480,  2874>,
        block_fft_implementation<60,   60,    4,    16,   960,  2875>,
        block_fft_implementation<30,   30,    8,    16,   480,  2877>,
        block_fft_implementation<30,   30,    8,    16,   960,  2876>
    >;
};

template<> struct block_fft_record<248, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    4,    64,   496,  2878>,
        block_fft_implementation<62,   62,    4,    16,   992,  2879>
    >;
};

template<> struct block_fft_record<252, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    6,   128,   504,  2880>,
        block_fft_implementation<42,   42,    6,    64,  1008,  2881>
    >;
};

template<> struct block_fft_record<272, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    8,    16,   544,  2883>,
        block_fft_implementation<34,   34,    8,    30,  1088,  2882>
    >;
};

template<> struct block_fft_record<288, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   12,    16,   576,  2884>,
        block_fft_implementation<24,   24,   12,    10,  1152,  2885>,
        block_fft_implementation<12,   12,   24,    10,   576,  2887>,
        block_fft_implementation<12,   12,   24,     8,  1152,  2886>,
        block_fft_implementation<36,   36,    8,     8,  1152,  2890>,
        block_fft_implementation<48,   48,    6,    10,   576,  2888>,
        block_fft_implementation< 6,    6,   48,     8,  1152,  2891>,
        block_fft_implementation<18,   18,   16,     8,  1152,  2889>,
        block_fft_implementation<48,   48,    6,    28,  1152,  2894>,
        block_fft_implementation<36,   36,    8,    96,   576,  2893>,
        block_fft_implementation< 6,    6,   48,     8,   576,  2892>,
        block_fft_implementation<18,   18,   16,    32,   576,  2895>
    >;
};

template<> struct block_fft_record<300, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   10,    24,   600,  2896>,
        block_fft_implementation<30,   30,   10,    12,  1200,  2897>,
        block_fft_implementation<60,   60,    5,    12,   600,  2898>,
        block_fft_implementation<60,   60,    5,    50,  1200,  2899>
    >;
};

template<> struct block_fft_record<304, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    8,    16,   608,  2901>,
        block_fft_implementation<38,   38,    8,     8,  1216,  2900>
    >;
};

template<> struct block_fft_record<320, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    8,     8,   640,  2902>,
        block_fft_implementation<20,   20,   16,     4,  1280,  2903>,
        block_fft_implementation<40,   40,    8,     8,  1280,  2905>,
        block_fft_implementation<20,   20,   16,     8,   640,  2904>,
        block_fft_implementation<10,   10,   32,     8,  1280,  2906>,
        block_fft_implementation<10,   10,   32,    16,   640,  2907>
    >;
};

template<> struct block_fft_record<336, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    8,     8,   672,  2909>,
        block_fft_implementation<42,   42,    8,     8,  1344,  2908>
    >;
};

template<> struct block_fft_record<352, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    8,    32,  1408,  2910>,
        block_fft_implementation<22,   22,   16,     8,  1408,  2911>,
        block_fft_implementation<44,   44,    8,     8,   704,  2912>,
        block_fft_implementation<22,   22,   16,    16,   704,  2913>
    >;
};

template<> struct block_fft_record<360, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    6,    42,   720,  2914>,
        block_fft_implementation<60,   60,    6,    20,  1440,  2916>,
        block_fft_implementation<30,   30,   12,    10,  1440,  2917>,
        block_fft_implementation<30,   30,   12,    16,   720,  2915>
    >;
};

template<> struct block_fft_record<368, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    8,    16,   736,  2918>,
        block_fft_implementation<46,   46,    8,    14,  1472,  2919>
    >;
};

template<> struct block_fft_record<384, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<48,   48,    8,    16,   768,  2923>,
        block_fft_implementation<24,   24,   16,     8,   768,  2922>,
        block_fft_implementation<24,   24,   16,     4,  1536,  2924>,
        block_fft_implementation<12,   12,   32,     4,   768,  2921>,
        block_fft_implementation<12,   12,   32,     2,  1536,  2920>,
        block_fft_implementation<48,   48,    8,    16,  1536,  2925>,
        block_fft_implementation< 6,    6,   64,     4,  1536,  2926>,
        block_fft_implementation< 6,    6,   64,     8,   768,  2927>
    >;
};

template<> struct block_fft_record<392, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   14,    18,   784,  2928>,
        block_fft_implementation<56,   56,    7,    18,   784,  2931>,
        block_fft_implementation<14,   14,   28,     2,  1568,  2930>,
        block_fft_implementation<28,   28,   14,    18,  1568,  2929>,
        block_fft_implementation<14,   14,   28,     2,   784,  2932>,
        block_fft_implementation<56,   56,    7,    36,  1568,  2933>
    >;
};

template<> struct block_fft_record<416, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   16,     8,  1664,  2935>,
        block_fft_implementation<52,   52,    8,    32,  1664,  2934>,
        block_fft_implementation<52,   52,    8,     8,   832,  2936>,
        block_fft_implementation<26,   26,   16,    12,   832,  2937>
    >;
};

template<> struct block_fft_record<432, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,   12,    20,   864,  2938>,
        block_fft_implementation<36,   36,   12,     8,  1728,  2940>,
        block_fft_implementation<12,   12,   36,    12,   864,  2941>,
        block_fft_implementation<12,   12,   36,     6,  1728,  2939>,
        block_fft_implementation<24,   24,   18,    14,   864,  2942>,
        block_fft_implementation< 6,    6,   72,     8,  1728,  2944>,
        block_fft_implementation<18,   18,   24,     8,  1728,  2943>,
        block_fft_implementation< 6,    6,   72,     8,   864,  2946>,
        block_fft_implementation<24,   24,   18,     6,  1728,  2945>,
        block_fft_implementation<48,   48,    9,    28,   864,  2948>,
        block_fft_implementation<18,   18,   24,    10,   864,  2947>,
        block_fft_implementation<54,   54,    8,    16,   864,  2951>,
        block_fft_implementation<54,   54,    8,     6,  1728,  2949>,
        block_fft_implementation<48,   48,    9,    28,  1728,  2950>
    >;
};

template<> struct block_fft_record<448, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    8,    16,   896,  2954>,
        block_fft_implementation<28,   28,   16,     8,  1792,  2952>,
        block_fft_implementation<28,   28,   16,    16,   896,  2953>,
        block_fft_implementation<56,   56,    8,     8,  1792,  2955>,
        block_fft_implementation<14,   14,   32,     2,  1792,  2956>,
        block_fft_implementation<14,   14,   32,     8,   896,  2957>
    >;
};

template<> struct block_fft_record<464, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    8,     8,   928,  2958>,
        block_fft_implementation<58,   58,    8,    10,  1856,  2959>
    >;
};

template<> struct block_fft_record<480, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   16,     8,  1920,  2960>,
        block_fft_implementation<60,   60,    8,    16,  1920,  2961>,
        block_fft_implementation<60,   60,    8,     8,   960,  2962>,
        block_fft_implementation<30,   30,   16,     8,   960,  2963>
    >;
};

template<> struct block_fft_record<496, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    8,     8,   992,  2964>,
        block_fft_implementation<62,   62,    8,    32,  1984,  2965>
    >;
};

template<> struct block_fft_record<500, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<50,   50,   10,    50,  1000,  2970>,
        block_fft_implementation<50,   50,   10,    12,  2000,  2971>,
        block_fft_implementation<10,   10,   50,    10,  2000,  2966>,
        block_fft_implementation<20,   20,   25,     2,  2000,  2968>,
        block_fft_implementation<10,   10,   50,    10,  1000,  2967>,
        block_fft_implementation<20,   20,   25,    10,  1000,  2969>
    >;
};

template<> struct block_fft_record<504, half, fft_type::c2c, fft_direction::inverse, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,   12,    10,  2016,  2972>,
        block_fft_implementation<42,   42,   12,    10,  1008,  2973>
    >;
};
