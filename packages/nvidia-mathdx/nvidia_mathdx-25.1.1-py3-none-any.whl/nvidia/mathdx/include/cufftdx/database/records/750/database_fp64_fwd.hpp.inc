//Copyright (c) 2019-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
//NVIDIA CORPORATION and its licensors retain all intellectual property
//and proprietary rights in and to this software, related documentation
//and any modifications thereto.  Any use, reproduction, disclosure or
//distribution of this software and related documentation without an express
//license agreement from NVIDIA CORPORATION is strictly prohibited.
//


template<> struct block_fft_record<33, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<33,   33,    1,    32,     0,  1022>
    >;
};

template<> struct block_fft_record<34, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    1,    32,     0,  1023>
    >;
};

template<> struct block_fft_record<35, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<35,   35,    1,    32,     0,  1024>
    >;
};

template<> struct block_fft_record<37, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<37,   37,    1,    32,     0,  1025>
    >;
};

template<> struct block_fft_record<38, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    1,    32,     0,  1026>
    >;
};

template<> struct block_fft_record<39, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<39,   39,    1,    32,     0,  1027>
    >;
};

template<> struct block_fft_record<40, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,    4,     8,   320,  1030>,
        block_fft_implementation<10,   10,    4,     8,   640,  1031>,
        block_fft_implementation<20,   20,    2,    16,   640,  1029>,
        block_fft_implementation<20,   20,    2,    16,   320,  1028>,
        block_fft_implementation<40,   40,    1,    32,     0,  1032>
    >;
};

template<> struct block_fft_record<2, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 2,    2,    1,    32,     0,  1033>
    >;
};

template<> struct block_fft_record<4, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4,    1,    32,     0,  1034>,
        block_fft_implementation< 2,    2,    2,    16,    32,  1035>,
        block_fft_implementation< 2,    2,    2,    16,    64,  1036>
    >;
};

template<> struct block_fft_record<8, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    1,    32,     0,  1037>,
        block_fft_implementation< 4,    4,    2,    16,    64,  1038>,
        block_fft_implementation< 2,    2,    4,     8,    64,  1039>,
        block_fft_implementation< 2,    2,    4,     8,   128,  1041>,
        block_fft_implementation< 4,    4,    2,    16,   128,  1040>
    >;
};

template<> struct block_fft_record<16, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    1,    32,     0,  1042>,
        block_fft_implementation< 4,    4,    4,     8,   128,  1044>,
        block_fft_implementation< 4,    4,    4,     8,   256,  1043>,
        block_fft_implementation< 2,    2,    8,     4,   128,  1048>,
        block_fft_implementation< 2,    2,    8,     4,   256,  1045>,
        block_fft_implementation< 8,    8,    2,    16,   128,  1046>,
        block_fft_implementation< 8,    8,    2,    16,   256,  1047>
    >;
};

template<> struct block_fft_record<32, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,    1,    32,     0,  1049>,
        block_fft_implementation< 8,    8,    4,     8,   256,  1050>,
        block_fft_implementation< 4,    4,    8,     4,   256,  1053>,
        block_fft_implementation< 2,    2,   16,     2,   256,  1056>,
        block_fft_implementation< 8,    8,    4,     8,   512,  1052>,
        block_fft_implementation< 2,    2,   16,     2,   512,  1055>,
        block_fft_implementation< 4,    4,    8,     4,   512,  1051>,
        block_fft_implementation<16,   16,    2,    16,   256,  1057>,
        block_fft_implementation<16,   16,    2,    16,   512,  1054>
    >;
};

template<> struct block_fft_record<64, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    8,     4,   512,  1058>,
        block_fft_implementation< 4,    4,   16,     2,   512,  1059>,
        block_fft_implementation< 4,    4,   16,     2,  1024,  1060>,
        block_fft_implementation< 8,    8,    8,     4,  1024,  1061>,
        block_fft_implementation<16,   16,    4,     8,   512,  1063>,
        block_fft_implementation< 2,    2,   32,     1,   512,  1065>,
        block_fft_implementation<16,   16,    4,     8,  1024,  1062>,
        block_fft_implementation< 2,    2,   32,     1,  1024,  1064>
    >;
};

template<> struct block_fft_record<128, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    8,     4,  1024,  1068>,
        block_fft_implementation<16,   16,    8,     4,  2048,  1067>,
        block_fft_implementation< 4,    4,   32,     1,  1024,  1070>,
        block_fft_implementation< 2,    2,   64,     1,  1024,  1073>,
        block_fft_implementation< 2,    2,   64,     1,  2048,  1072>,
        block_fft_implementation< 4,    4,   32,     1,  2048,  1069>,
        block_fft_implementation< 8,    8,   16,     2,  1024,  1066>,
        block_fft_implementation< 8,    8,   16,     2,  2048,  1071>
    >;
};

template<> struct block_fft_record<256, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4,   64,     1,  2048,  1078>,
        block_fft_implementation<16,   16,   16,     2,  2048,  1076>,
        block_fft_implementation< 4,    4,   64,     1,  4096,  1077>,
        block_fft_implementation<16,   16,   16,     2,  4096,  1075>,
        block_fft_implementation< 8,    8,   32,     1,  2048,  1074>,
        block_fft_implementation< 2,    2,  128,     1,  2048,  1080>,
        block_fft_implementation< 8,    8,   32,     1,  4096,  1079>,
        block_fft_implementation< 2,    2,  128,     1,  4096,  1081>
    >;
};

template<> struct block_fft_record<512, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,   64,     1,  4096,  1082>,
        block_fft_implementation< 8,    8,   64,     1,  8192,  1083>,
        block_fft_implementation< 4,    4,  128,     1,  4096,  1086>,
        block_fft_implementation< 4,    4,  128,     1,  8192,  1087>,
        block_fft_implementation< 2,    2,  256,     1,  4096,  1088>,
        block_fft_implementation< 2,    2,  256,     1,  8192,  1089>,
        block_fft_implementation<16,   16,   32,     1,  4096,  1085>,
        block_fft_implementation<16,   16,   32,     1,  8192,  1084>
    >;
};

template<> struct block_fft_record<1024, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4,  256,     1,  8192,  1092>,
        block_fft_implementation< 4,    4,  256,     1, 16384,  1093>,
        block_fft_implementation<16,   16,   64,     1,  8192,  1091>,
        block_fft_implementation< 2,    2,  512,     1, 16384,  1096>,
        block_fft_implementation<16,   16,   64,     1, 16384,  1094>,
        block_fft_implementation< 2,    2,  512,     1,  8192,  1097>,
        block_fft_implementation< 8,    8,  128,     1,  8192,  1090>,
        block_fft_implementation< 8,    8,  128,     1, 16384,  1095>
    >;
};

template<> struct block_fft_record<2048, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,  128,     1, 16384,  1099>,
        block_fft_implementation< 4,    4,  512,     1, 16384,  1102>,
        block_fft_implementation< 8,    8,  256,     1, 16384,  1098>,
        block_fft_implementation<16,   16,  128,     1, 32768,  1100>,
        block_fft_implementation< 4,    4,  512,     1, 32768,  1103>,
        block_fft_implementation< 2,    2, 1024,     1, 32768,  1105>,
        block_fft_implementation< 8,    8,  256,     1, 32768,  1101>,
        block_fft_implementation< 2,    2, 1024,     1, 16384,  1104>
    >;
};

template<> struct block_fft_record<4096, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4, 1024,     1, 32768,  1110>,
        block_fft_implementation< 4,    4, 1024,     1, 65536,  1111>,
        block_fft_implementation<16,   16,  256,     1, 65536,  1108>,
        block_fft_implementation< 8,    8,  512,     1, 32768,  1106>,
        block_fft_implementation<16,   16,  256,     1, 32768,  1107>,
        block_fft_implementation< 8,    8,  512,     1, 65536,  1109>
    >;
};

template<> struct block_fft_record<8192, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8, 1024,     1, 65536,  1113>,
        block_fft_implementation<16,   16,  512,     1, 65536,  1112>
    >;
};

template<> struct block_fft_record<3, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,    1,    32,     0,  1114>
    >;
};

template<> struct block_fft_record<9, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    1,    32,     0,  1115>,
        block_fft_implementation< 3,    3,    3,    32,    72,  1116>,
        block_fft_implementation< 3,    3,    3,    32,   144,  1117>
    >;
};

template<> struct block_fft_record<27, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    1,    32,     0,  1118>,
        block_fft_implementation< 3,    3,    9,     7,   216,  1121>,
        block_fft_implementation< 3,    3,    9,     7,   432,  1122>,
        block_fft_implementation< 9,    9,    3,    32,   216,  1119>,
        block_fft_implementation< 9,    9,    3,    32,   432,  1120>
    >;
};

template<> struct block_fft_record<81, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,   27,     7,   648,  1128>,
        block_fft_implementation< 3,    3,   27,    13,  1296,  1127>,
        block_fft_implementation< 9,    9,    9,    32,   648,  1124>,
        block_fft_implementation< 9,    9,    9,    32,  1296,  1123>,
        block_fft_implementation<27,   27,    3,    32,   648,  1125>,
        block_fft_implementation<27,   27,    3,    32,  1296,  1126>
    >;
};

template<> struct block_fft_record<243, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,   81,    11,  3888,  1133>,
        block_fft_implementation< 3,    3,   81,     5,  1944,  1134>,
        block_fft_implementation<27,   27,    9,     7,  1944,  1129>,
        block_fft_implementation<27,   27,    9,     7,  3888,  1130>,
        block_fft_implementation< 9,    9,   27,    13,  1944,  1132>,
        block_fft_implementation< 9,    9,   27,    13,  3888,  1131>
    >;
};

template<> struct block_fft_record<729, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,  243,     3, 11664,  1140>,
        block_fft_implementation< 3,    3,  243,     3,  5832,  1139>,
        block_fft_implementation<27,   27,   27,     7,  5832,  1137>,
        block_fft_implementation< 9,    9,   81,    11,  5832,  1136>,
        block_fft_implementation< 9,    9,   81,     5, 11664,  1135>,
        block_fft_implementation<27,   27,   27,     2, 11664,  1138>
    >;
};

template<> struct block_fft_record<2187, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,  729,     1, 34992,  1144>,
        block_fft_implementation< 3,    3,  729,     1, 17496,  1143>,
        block_fft_implementation< 9,    9,  243,     3, 17496,  1141>,
        block_fft_implementation< 9,    9,  243,     1, 34992,  1142>
    >;
};

template<> struct block_fft_record<6561, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,  729,     1, 52488,  1145>
    >;
};

template<> struct block_fft_record<5, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,    1,    32,     0,  1146>
    >;
};

template<> struct block_fft_record<25, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    1,    32,     0,  1147>,
        block_fft_implementation< 5,    5,    5,    32,   200,  1149>,
        block_fft_implementation< 5,    5,    5,    32,   400,  1148>
    >;
};

template<> struct block_fft_record<125, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,   25,    14,  1000,  1151>,
        block_fft_implementation<25,   25,    5,    19,  1000,  1152>,
        block_fft_implementation< 5,    5,   25,    14,  2000,  1150>,
        block_fft_implementation<25,   25,    5,    32,  2000,  1153>
    >;
};

template<> struct block_fft_record<625, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,   25,     5,  5000,  1154>,
        block_fft_implementation<25,   25,   25,     5, 10000,  1157>,
        block_fft_implementation< 5,    5,  125,     1,  5000,  1155>,
        block_fft_implementation< 5,    5,  125,     1, 10000,  1156>
    >;
};

template<> struct block_fft_record<3125, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,  625,     1, 25000,  1159>,
        block_fft_implementation< 5,    5,  625,     1, 50000,  1158>
    >;
};

template<> struct block_fft_record<7, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    1,    32,     0,  1160>
    >;
};

template<> struct block_fft_record<49, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    7,    32,   392,  1161>,
        block_fft_implementation< 7,    7,    7,    32,   784,  1162>
    >;
};

template<> struct block_fft_record<343, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,   49,    13,  2744,  1164>,
        block_fft_implementation< 7,    7,   49,     9,  5488,  1163>
    >;
};

template<> struct block_fft_record<2401, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,  343,     1, 19208,  1166>,
        block_fft_implementation< 7,    7,  343,     1, 38416,  1165>
    >;
};

template<> struct block_fft_record<11, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,    1,    32,     0,  1167>
    >;
};

template<> struct block_fft_record<121, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,   11,    29,   968,  1169>,
        block_fft_implementation<11,   11,   11,    29,  1936,  1168>
    >;
};

template<> struct block_fft_record<1331, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,  121,     5, 10648,  1170>,
        block_fft_implementation<11,   11,  121,     1, 21296,  1171>
    >;
};

template<> struct block_fft_record<6, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    1,    32,     0,  1172>
    >;
};

template<> struct block_fft_record<36, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    6,    16,   288,  1174>,
        block_fft_implementation< 6,    6,    6,    16,   576,  1173>,
        block_fft_implementation<36,   36,    1,    32,     0,  1175>
    >;
};

template<> struct block_fft_record<216, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,   36,     8,  1728,  1176>,
        block_fft_implementation< 6,    6,   36,     8,  3456,  1177>
    >;
};

template<> struct block_fft_record<1296, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,  216,     4, 10368,  1178>,
        block_fft_implementation< 6,    6,  216,     1, 20736,  1179>
    >;
};

template<> struct block_fft_record<7776, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,  216,     1, 62208,  1180>
    >;
};

template<> struct block_fft_record<10, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,    1,    32,     0,  1181>
    >;
};

template<> struct block_fft_record<100, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,   10,    16,   800,  1183>,
        block_fft_implementation<10,   10,   10,    16,  1600,  1182>
    >;
};

template<> struct block_fft_record<1000, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,  100,     6,  8000,  1185>,
        block_fft_implementation<10,   10,  100,     3, 16000,  1184>
    >;
};

template<> struct block_fft_record<12, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    1,    32,     0,  1187>
    >;
};

template<> struct block_fft_record<144, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,   12,     8,  1152,  1188>,
        block_fft_implementation<12,   12,   12,     8,  2304,  1189>
    >;
};

template<> struct block_fft_record<1728, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,  144,     2, 13824,  1190>,
        block_fft_implementation<12,   12,  144,     2, 27648,  1191>
    >;
};

template<> struct block_fft_record<13, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,    1,    32,     0,  1192>
    >;
};

template<> struct block_fft_record<169, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,   13,    22,  1352,  1193>,
        block_fft_implementation<13,   13,   13,    22,  2704,  1194>
    >;
};

template<> struct block_fft_record<2197, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,  169,     3, 17576,  1195>,
        block_fft_implementation<13,   13,  169,     1, 35152,  1196>
    >;
};

template<> struct block_fft_record<14, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,    1,    32,     0,  1197>
    >;
};

template<> struct block_fft_record<196, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,   14,    16,  1568,  1198>,
        block_fft_implementation<14,   14,   14,    16,  3136,  1199>
    >;
};

template<> struct block_fft_record<2744, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,  196,     2, 21952,  1201>,
        block_fft_implementation<14,   14,  196,     1, 43904,  1200>
    >;
};

template<> struct block_fft_record<15, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,    1,    32,     0,  1202>
    >;
};

template<> struct block_fft_record<225, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,   15,    17,  1800,  1203>,
        block_fft_implementation<15,   15,   15,    17,  3600,  1204>
    >;
};

template<> struct block_fft_record<3375, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,  225,     2, 27000,  1205>,
        block_fft_implementation<15,   15,  225,     1, 54000,  1206>
    >;
};

template<> struct block_fft_record<17, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,    1,    32,     0,  1207>
    >;
};

template<> struct block_fft_record<289, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,   17,    13,  2312,  1208>,
        block_fft_implementation<17,   17,   17,    13,  4624,  1209>
    >;
};

template<> struct block_fft_record<4913, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,  289,     1, 39304,  1210>
    >;
};

template<> struct block_fft_record<18, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    1,    32,     0,  1212>
    >;
};

template<> struct block_fft_record<324, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,   18,     7,  2592,  1213>,
        block_fft_implementation<18,   18,   18,     7,  5184,  1214>
    >;
};

template<> struct block_fft_record<5832, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,  324,     1, 46656,  1215>
    >;
};

template<> struct block_fft_record<19, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,    1,    32,     0,  1217>
    >;
};

template<> struct block_fft_record<361, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,   19,     5,  2888,  1218>,
        block_fft_implementation<19,   19,   19,     5,  5776,  1219>
    >;
};

template<> struct block_fft_record<6859, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,  361,     1, 54872,  1220>
    >;
};

template<> struct block_fft_record<20, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    1,    32,     0,  1221>
    >;
};

template<> struct block_fft_record<400, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   20,     8,  3200,  1222>,
        block_fft_implementation<20,   20,   20,     8,  6400,  1223>
    >;
};

template<> struct block_fft_record<8000, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,  400,     1, 64000,  1224>
    >;
};

template<> struct block_fft_record<21, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,    1,    32,     0,  1225>
    >;
};

template<> struct block_fft_record<441, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,   21,     3,  3528,  1226>,
        block_fft_implementation<21,   21,   21,     3,  7056,  1227>
    >;
};

template<> struct block_fft_record<22, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    1,    32,     0,  1229>
    >;
};

template<> struct block_fft_record<484, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,   22,    13,  3872,  1230>,
        block_fft_implementation<22,   22,   22,     7,  7744,  1231>
    >;
};

template<> struct block_fft_record<23, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,    1,    32,     0,  1233>
    >;
};

template<> struct block_fft_record<529, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,   23,    11,  4232,  1235>,
        block_fft_implementation<23,   23,   23,     4,  8464,  1234>
    >;
};

template<> struct block_fft_record<24, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    1,    32,     0,  1237>
    >;
};

template<> struct block_fft_record<576, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   24,     4,  4608,  1238>,
        block_fft_implementation<24,   24,   24,     4,  9216,  1239>
    >;
};

template<> struct block_fft_record<26, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    1,    32,     0,  1240>
    >;
};

template<> struct block_fft_record<676, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   26,    11,  5408,  1241>,
        block_fft_implementation<26,   26,   26,     6, 10816,  1242>
    >;
};

template<> struct block_fft_record<28, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    1,    32,     0,  1243>
    >;
};

template<> struct block_fft_record<784, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   28,     8,  6272,  1244>,
        block_fft_implementation<28,   28,   28,     2, 12544,  1245>
    >;
};

template<> struct block_fft_record<29, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,    1,    32,     0,  1246>
    >;
};

template<> struct block_fft_record<841, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,   29,     1,  6728,  1247>,
        block_fft_implementation<29,   29,   29,     1, 13456,  1248>
    >;
};

template<> struct block_fft_record<30, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    1,    32,     0,  1249>
    >;
};

template<> struct block_fft_record<900, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   30,     1,  7200,  1250>,
        block_fft_implementation<30,   30,   30,     1, 14400,  1251>
    >;
};

template<> struct block_fft_record<31, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,    1,    32,     0,  1252>
    >;
};

template<> struct block_fft_record<961, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,   31,     1,  7688,  1253>,
        block_fft_implementation<31,   31,   31,     1, 15376,  1254>
    >;
};

template<> struct block_fft_record<44, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    2,    16,   352,  1255>,
        block_fft_implementation<22,   22,    2,    32,   704,  1256>
    >;
};

template<> struct block_fft_record<48, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    4,     8,   384,  1257>,
        block_fft_implementation<12,   12,    4,     8,   768,  1258>,
        block_fft_implementation< 6,    6,    8,     4,   384,  1262>,
        block_fft_implementation< 6,    6,    8,     4,   768,  1259>,
        block_fft_implementation<24,   24,    2,    16,   384,  1260>,
        block_fft_implementation<24,   24,    2,    16,   768,  1261>
    >;
};

template<> struct block_fft_record<52, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    2,    32,   416,  1263>,
        block_fft_implementation<26,   26,    2,    16,   832,  1264>
    >;
};

template<> struct block_fft_record<56, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,    4,     8,   448,  1266>,
        block_fft_implementation<28,   28,    2,    16,   448,  1265>,
        block_fft_implementation<14,   14,    4,    16,   896,  1267>,
        block_fft_implementation<28,   28,    2,    16,   896,  1268>
    >;
};

template<> struct block_fft_record<60, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    2,    16,   480,  1269>,
        block_fft_implementation<30,   30,    2,    16,   960,  1270>
    >;
};

template<> struct block_fft_record<68, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    2,    16,   544,  1271>,
        block_fft_implementation<34,   34,    2,    16,  1088,  1272>
    >;
};

template<> struct block_fft_record<72, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    6,    16,   576,  1273>,
        block_fft_implementation<24,   24,    3,    32,   576,  1275>,
        block_fft_implementation<12,   12,    6,    16,  1152,  1274>,
        block_fft_implementation<18,   18,    4,     8,   576,  1277>,
        block_fft_implementation<36,   36,    2,    16,   576,  1276>,
        block_fft_implementation< 6,    6,   12,     8,   576,  1278>,
        block_fft_implementation<18,   18,    4,     8,  1152,  1280>,
        block_fft_implementation<36,   36,    2,    16,  1152,  1282>,
        block_fft_implementation< 6,    6,   12,     8,  1152,  1279>,
        block_fft_implementation<24,   24,    3,    10,  1152,  1281>
    >;
};

template<> struct block_fft_record<76, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    2,    16,   608,  1283>,
        block_fft_implementation<38,   38,    2,    16,  1216,  1284>
    >;
};

template<> struct block_fft_record<80, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    4,     8,   640,  1285>,
        block_fft_implementation<20,   20,    4,     8,  1280,  1286>,
        block_fft_implementation<10,   10,    8,     4,   640,  1289>,
        block_fft_implementation<10,   10,    8,     4,  1280,  1287>,
        block_fft_implementation<40,   40,    2,    16,   640,  1288>,
        block_fft_implementation<40,   40,    2,    16,  1280,  1290>
    >;
};

template<> struct block_fft_record<84, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    2,    16,   672,  1291>,
        block_fft_implementation<42,   42,    2,    16,  1344,  1292>
    >;
};

template<> struct block_fft_record<88, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    4,     8,   704,  1293>,
        block_fft_implementation<44,   44,    2,    32,   704,  1294>,
        block_fft_implementation<22,   22,    4,    16,  1408,  1295>,
        block_fft_implementation<44,   44,    2,    16,  1408,  1296>
    >;
};

template<> struct block_fft_record<92, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    2,    32,   736,  1297>,
        block_fft_implementation<46,   46,    2,    16,  1472,  1298>
    >;
};

template<> struct block_fft_record<96, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    4,     8,   768,  1299>,
        block_fft_implementation< 6,    6,   16,     2,   768,  1303>,
        block_fft_implementation<12,   12,    8,     4,   768,  1300>,
        block_fft_implementation< 6,    6,   16,     2,  1536,  1304>,
        block_fft_implementation<24,   24,    4,     8,  1536,  1302>,
        block_fft_implementation<12,   12,    8,     4,  1536,  1301>,
        block_fft_implementation<48,   48,    2,    16,   768,  1305>,
        block_fft_implementation<48,   48,    2,    16,  1536,  1306>
    >;
};

template<> struct block_fft_record<104, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    4,     8,   832,  1307>,
        block_fft_implementation<52,   52,    2,    16,   832,  1308>,
        block_fft_implementation<26,   26,    4,     8,  1664,  1309>,
        block_fft_implementation<52,   52,    2,    16,  1664,  1310>
    >;
};

template<> struct block_fft_record<108, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    6,    16,   864,  1311>,
        block_fft_implementation<12,   12,    9,     7,   864,  1317>,
        block_fft_implementation<36,   36,    3,    32,   864,  1314>,
        block_fft_implementation<18,   18,    6,    16,  1728,  1312>,
        block_fft_implementation< 6,    6,   18,    16,   864,  1313>,
        block_fft_implementation<12,   12,    9,     7,  1728,  1318>,
        block_fft_implementation<54,   54,    2,    16,   864,  1316>,
        block_fft_implementation< 6,    6,   18,    16,  1728,  1315>,
        block_fft_implementation<36,   36,    3,    32,  1728,  1319>,
        block_fft_implementation<54,   54,    2,    16,  1728,  1320>
    >;
};

template<> struct block_fft_record<112, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    4,     8,   896,  1321>,
        block_fft_implementation<28,   28,    4,     8,  1792,  1323>,
        block_fft_implementation<14,   14,    8,     4,   896,  1324>,
        block_fft_implementation<56,   56,    2,    16,   896,  1325>,
        block_fft_implementation<14,   14,    8,     8,  1792,  1322>,
        block_fft_implementation<56,   56,    2,    16,  1792,  1326>
    >;
};

template<> struct block_fft_record<116, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    2,    16,   928,  1327>,
        block_fft_implementation<58,   58,    2,    16,  1856,  1328>
    >;
};

template<> struct block_fft_record<120, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    4,     8,   960,  1329>,
        block_fft_implementation<60,   60,    2,    16,   960,  1330>,
        block_fft_implementation<30,   30,    4,     8,  1920,  1331>,
        block_fft_implementation<60,   60,    2,    16,  1920,  1332>
    >;
};

template<> struct block_fft_record<124, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    2,    16,   992,  1333>,
        block_fft_implementation<62,   62,    2,    16,  1984,  1334>
    >;
};

template<> struct block_fft_record<136, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    4,     8,  1088,  1335>,
        block_fft_implementation<34,   34,    4,     8,  2176,  1336>
    >;
};

template<> struct block_fft_record<152, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    4,     8,  1216,  1337>,
        block_fft_implementation<38,   38,    4,     8,  2432,  1338>
    >;
};

template<> struct block_fft_record<160, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    4,     8,  1280,  1340>,
        block_fft_implementation<10,   10,   16,     2,  1280,  1343>,
        block_fft_implementation<40,   40,    4,     8,  2560,  1344>,
        block_fft_implementation<20,   20,    8,     4,  1280,  1339>,
        block_fft_implementation<10,   10,   16,     2,  2560,  1342>,
        block_fft_implementation<20,   20,    8,     4,  2560,  1341>
    >;
};

template<> struct block_fft_record<168, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    4,     8,  1344,  1345>,
        block_fft_implementation<42,   42,    4,     8,  2688,  1346>
    >;
};

template<> struct block_fft_record<176, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    4,    16,  1408,  1347>,
        block_fft_implementation<44,   44,    4,     8,  2816,  1350>,
        block_fft_implementation<22,   22,    8,     4,  1408,  1349>,
        block_fft_implementation<22,   22,    8,     8,  2816,  1348>
    >;
};

template<> struct block_fft_record<180, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    6,    16,  1440,  1351>,
        block_fft_implementation<60,   60,    3,    21,  1440,  1353>,
        block_fft_implementation<30,   30,    6,    16,  2880,  1352>,
        block_fft_implementation<60,   60,    3,    21,  2880,  1354>
    >;
};

template<> struct block_fft_record<184, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    4,    16,  1472,  1355>,
        block_fft_implementation<46,   46,    4,     8,  2944,  1356>
    >;
};

template<> struct block_fft_record<192, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    8,     4,  1536,  1358>,
        block_fft_implementation<12,   12,   16,     2,  1536,  1357>,
        block_fft_implementation<12,   12,   16,     2,  3072,  1359>,
        block_fft_implementation< 6,    6,   32,     1,  1536,  1362>,
        block_fft_implementation<24,   24,    8,     4,  3072,  1360>,
        block_fft_implementation<48,   48,    4,     8,  1536,  1361>,
        block_fft_implementation<48,   48,    4,     8,  3072,  1364>,
        block_fft_implementation< 6,    6,   32,     1,  3072,  1363>
    >;
};

template<> struct block_fft_record<200, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   10,    16,  1600,  1365>,
        block_fft_implementation<40,   40,    5,    19,  1600,  1368>,
        block_fft_implementation<20,   20,   10,    16,  3200,  1366>,
        block_fft_implementation<50,   50,    4,    16,  1600,  1370>,
        block_fft_implementation<50,   50,    4,     8,  3200,  1372>,
        block_fft_implementation<10,   10,   20,     8,  1600,  1367>,
        block_fft_implementation<40,   40,    5,     6,  3200,  1371>,
        block_fft_implementation<10,   10,   20,     8,  3200,  1369>
    >;
};

template<> struct block_fft_record<208, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    4,     8,  1664,  1373>,
        block_fft_implementation<52,   52,    4,     8,  3328,  1376>,
        block_fft_implementation<26,   26,    8,     4,  1664,  1375>,
        block_fft_implementation<26,   26,    8,     4,  3328,  1374>
    >;
};

template<> struct block_fft_record<224, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    4,    16,  1792,  1379>,
        block_fft_implementation<14,   14,   16,     2,  1792,  1378>,
        block_fft_implementation<28,   28,    8,     4,  1792,  1377>,
        block_fft_implementation<14,   14,   16,     4,  3584,  1380>,
        block_fft_implementation<28,   28,    8,     4,  3584,  1381>,
        block_fft_implementation<56,   56,    4,     8,  3584,  1382>
    >;
};

template<> struct block_fft_record<232, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    4,     8,  1856,  1383>,
        block_fft_implementation<58,   58,    4,     8,  3712,  1384>
    >;
};

template<> struct block_fft_record<240, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    4,     8,  1920,  1385>,
        block_fft_implementation<30,   30,    8,     4,  1920,  1386>,
        block_fft_implementation<60,   60,    4,     8,  3840,  1388>,
        block_fft_implementation<30,   30,    8,     4,  3840,  1387>
    >;
};

template<> struct block_fft_record<248, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    4,     8,  1984,  1389>,
        block_fft_implementation<62,   62,    4,     8,  3968,  1390>
    >;
};

template<> struct block_fft_record<252, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    6,    16,  2016,  1391>,
        block_fft_implementation<42,   42,    6,    16,  4032,  1392>
    >;
};

template<> struct block_fft_record<272, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    8,     4,  2176,  1393>,
        block_fft_implementation<34,   34,    8,     4,  4352,  1394>
    >;
};

template<> struct block_fft_record<288, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   12,     8,  2304,  1395>,
        block_fft_implementation<36,   36,    8,     4,  2304,  1397>,
        block_fft_implementation<18,   18,   16,     2,  2304,  1399>,
        block_fft_implementation< 6,    6,   48,     2,  2304,  1400>,
        block_fft_implementation<18,   18,   16,     2,  4608,  1401>,
        block_fft_implementation<48,   48,    6,    16,  2304,  1403>,
        block_fft_implementation<36,   36,    8,     4,  4608,  1405>,
        block_fft_implementation<24,   24,   12,     5,  4608,  1402>,
        block_fft_implementation< 6,    6,   48,     2,  4608,  1404>,
        block_fft_implementation<12,   12,   24,     4,  2304,  1396>,
        block_fft_implementation<48,   48,    6,     5,  4608,  1406>,
        block_fft_implementation<12,   12,   24,     4,  4608,  1398>
    >;
};

template<> struct block_fft_record<300, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   10,    16,  2400,  1407>,
        block_fft_implementation<60,   60,    5,    19,  2400,  1408>,
        block_fft_implementation<30,   30,   10,     3,  4800,  1409>,
        block_fft_implementation<60,   60,    5,    12,  4800,  1410>
    >;
};

template<> struct block_fft_record<304, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    8,     4,  2432,  1411>,
        block_fft_implementation<38,   38,    8,     4,  4864,  1412>
    >;
};

template<> struct block_fft_record<320, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    8,     4,  2560,  1414>,
        block_fft_implementation<20,   20,   16,     2,  2560,  1413>,
        block_fft_implementation<40,   40,    8,     4,  5120,  1418>,
        block_fft_implementation<20,   20,   16,     2,  5120,  1415>,
        block_fft_implementation<10,   10,   32,     1,  2560,  1417>,
        block_fft_implementation<10,   10,   32,     1,  5120,  1416>
    >;
};

template<> struct block_fft_record<336, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    8,     4,  2688,  1419>,
        block_fft_implementation<42,   42,    8,     4,  5376,  1420>
    >;
};

template<> struct block_fft_record<352, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    8,     8,  2816,  1421>,
        block_fft_implementation<22,   22,   16,     2,  2816,  1423>,
        block_fft_implementation<22,   22,   16,     4,  5632,  1422>,
        block_fft_implementation<44,   44,    8,     4,  5632,  1424>
    >;
};

template<> struct block_fft_record<360, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    6,    16,  2880,  1426>,
        block_fft_implementation<30,   30,   12,     8,  2880,  1425>,
        block_fft_implementation<30,   30,   12,     8,  5760,  1427>,
        block_fft_implementation<60,   60,    6,    10,  5760,  1428>
    >;
};

template<> struct block_fft_record<368, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    8,     8,  2944,  1429>,
        block_fft_implementation<46,   46,    8,     4,  5888,  1430>
    >;
};

template<> struct block_fft_record<384, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<48,   48,    8,     4,  3072,  1434>,
        block_fft_implementation<48,   48,    8,     4,  6144,  1438>,
        block_fft_implementation< 6,    6,   64,     1,  3072,  1436>,
        block_fft_implementation<12,   12,   32,     1,  3072,  1431>,
        block_fft_implementation< 6,    6,   64,     1,  6144,  1437>,
        block_fft_implementation<12,   12,   32,     1,  6144,  1433>,
        block_fft_implementation<24,   24,   16,     2,  3072,  1432>,
        block_fft_implementation<24,   24,   16,     2,  6144,  1435>
    >;
};

template<> struct block_fft_record<392, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   14,     9,  3136,  1439>,
        block_fft_implementation<56,   56,    7,     9,  3136,  1443>,
        block_fft_implementation<28,   28,   14,     9,  6272,  1442>,
        block_fft_implementation<14,   14,   28,     8,  3136,  1440>,
        block_fft_implementation<14,   14,   28,     8,  6272,  1441>,
        block_fft_implementation<56,   56,    7,     8,  6272,  1444>
    >;
};

template<> struct block_fft_record<416, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   16,     2,  3328,  1446>,
        block_fft_implementation<52,   52,    8,     4,  3328,  1445>,
        block_fft_implementation<26,   26,   16,     2,  6656,  1447>,
        block_fft_implementation<52,   52,    8,     4,  6656,  1448>
    >;
};

template<> struct block_fft_record<432, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,   12,     8,  3456,  1449>,
        block_fft_implementation<36,   36,   12,     8,  6912,  1458>,
        block_fft_implementation<54,   54,    8,     4,  3456,  1459>,
        block_fft_implementation<12,   12,   36,     8,  3456,  1450>,
        block_fft_implementation<24,   24,   18,     7,  3456,  1452>,
        block_fft_implementation<18,   18,   24,     4,  3456,  1454>,
        block_fft_implementation< 6,    6,   72,     4,  3456,  1451>,
        block_fft_implementation<12,   12,   36,     8,  6912,  1453>,
        block_fft_implementation<48,   48,    9,     7,  3456,  1460>,
        block_fft_implementation<18,   18,   24,     4,  6912,  1455>,
        block_fft_implementation< 6,    6,   72,     4,  6912,  1456>,
        block_fft_implementation<48,   48,    9,     7,  6912,  1462>,
        block_fft_implementation<24,   24,   18,     7,  6912,  1457>,
        block_fft_implementation<54,   54,    8,     4,  6912,  1461>
    >;
};

template<> struct block_fft_record<448, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    8,     4,  3584,  1464>,
        block_fft_implementation<28,   28,   16,     2,  3584,  1463>,
        block_fft_implementation<56,   56,    8,     4,  7168,  1468>,
        block_fft_implementation<28,   28,   16,     2,  7168,  1465>,
        block_fft_implementation<14,   14,   32,     1,  3584,  1467>,
        block_fft_implementation<14,   14,   32,     2,  7168,  1466>
    >;
};

template<> struct block_fft_record<464, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    8,     4,  3712,  1469>,
        block_fft_implementation<58,   58,    8,     4,  7424,  1470>
    >;
};

template<> struct block_fft_record<480, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   16,     2,  3840,  1471>,
        block_fft_implementation<60,   60,    8,     4,  3840,  1472>,
        block_fft_implementation<30,   30,   16,     2,  7680,  1473>,
        block_fft_implementation<60,   60,    8,     4,  7680,  1474>
    >;
};

template<> struct block_fft_record<496, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    8,     4,  3968,  1475>,
        block_fft_implementation<62,   62,    8,     4,  7936,  1476>
    >;
};

template<> struct block_fft_record<500, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<50,   50,   10,    16,  4000,  1478>,
        block_fft_implementation<20,   20,   25,     5,  4000,  1479>,
        block_fft_implementation<10,   10,   50,     7,  4000,  1477>,
        block_fft_implementation<10,   10,   50,     7,  8000,  1480>,
        block_fft_implementation<50,   50,   10,     3,  8000,  1482>,
        block_fft_implementation<20,   20,   25,     5,  8000,  1481>
    >;
};

template<> struct block_fft_record<504, double, fft_type::c2c, fft_direction::forward, 750> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,   12,     8,  4032,  1483>,
        block_fft_implementation<42,   42,   12,     8,  8064,  1484>
    >;
};
