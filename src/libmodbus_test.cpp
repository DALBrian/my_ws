#include <errno.h>
// #include <modbus.h>
#include "/usr/local/include/modbus/modbus.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <iostream>
using namespace std;
/**
 * @brief: Use libmodbus to connect to modbus TCP device. Prior test use only.
 * @author: Small Brian
 * @date: 20230324
 * **/


enum{
    TCP,
    TCP_PI,
    RTU
};
int main(int argc, char **argv){
    int s;
    modbus_t *ctx;
    modbus_mapping_t *mb_mapping;
    int rc;
    int i;
    int use_backend;
    uint8_t *query;
    int header_length;
    char *ip_or_device;

    if (argc > 1){
        if (strcmp(argv[1], "tcp") == 0){
            use_backend = TCP;
        }
        else if (strcmp(argv[1], "rtu") == 0){
            use_backend = RTU;
        }
        else{
            printf("Modbus server for unit testing.\n");
            printf("Usage:\n  %s [tcp|tcppi|rtu] [<ip or device>]\n", argv[0]);
            printf("Eg. tcp 127.0.0.1 or rtu /dev/ttyUSB0\n\n");
            return -1;
        }
    }
    else{
        use_backend = TCP;
    }
    if (argc > 2){
        ip_or_device = argv[2];
    }
    else{
        // ip_or_device = "127.0.0.1";
        ip_or_device = "192.168.255.1"; //Using ICPDAS device for testing
    }
    if (use_backend == TCP){
        ctx = modbus_new_tcp(ip_or_device, 1502);
        query = malloc(MODBUS_TCP_MAX_ADU_LENGTH);
    }
    else{
        ctx = modbus_new_rtu(ip_or_device, 1152000, 'N', 8, 1);
        modbus_set_slave(ctx,   server_ID);
    }
    header_length = modbus_get_header_length(ctx);
    modbus_set_debug(ctx, TRUE);
    mb_mapping = modbus_mapping_new_start_address(UT_BITS_ADDRESS, UT_BITS_NB,
                                                UT_INPUT_BITS_ADDRESS, UT_INPUT_BITS_NB, 
                                                UT_REGISTERS_ADDRESS, UT_REGISTERS_NB_MAX,
                                                UT_INPUT_REGISTERS_ADDRESS, UT_INPUT_REGISTERS_NB);
    if (mb_mapping == NULL){
        fprintf(stderr, "Failed to allocate the mapping: %s\n", modbus_strerror(errno));
        modbus_free(ctx);
        return -1;
    }
     modbus_set_bits_from_bytes(
        mb_mapping->tab_input_bits, 0, UT_INPUT_BITS_NB, UT_INPUT_BITS_TAB);
    for (i = 0; i < UT_INPUT_REGISTERS_NB; i++){
        mb_mapping->tab_input_registers[i] = UT_INPUT_REGISTERES_TAB[i];
    }
    if (use_backend == TCP){
        s = modbus_tcp_listen(ctx, 1);
        modbus_tcp_accept(ctx, &s);
    }
    else{
        rc = modbus_connect(ctx);
        if (rc == -1){
           fprintf(stderr, "Unable to connect %s\n", modbus_strerror(errno));
            modbus_free(ctx);
            return -1; 
        }
    }
    for (;;){
        do{
            rc = modbus_receive(ctx, query);
        }while(rc == 0);
        if (rc == -1 && errno != EMBBADCRC){
            break;
        }
        if (query[header_length] == 0x33){
            if (MODBUS_GET_INT16_FROM_INT8(query, header_length + 3) ==
                        UT_REGISTERS_NB_SPECIAL){
                printf("Set an incorrect no. of values\n");
                MODBUS_GET_INT16_FROM_INT8(query, header_length + 3, UT_REGISTERS_NB_SPECIAL - 1);
            }else if(MODBUS_GET_INT16_FROM_INT8(query, header_length + 1) ==
                        UT_REGISTERS_ADDRESS_INVALID_TID_OR_SLAVE){
                const int RAW_REQ_LENGTH = 5;
                uint8_t raw_req[] = {(use_backend == RTU) ? INVALID_SERVER_ID: 0xFF,
                    0x03,
                    0x02,
                    0x00,
                    0x00};
                printf("Reply with invalid TID or slave\n");
                modbus_send_raw_request(ctx, raw_req, RAW_REQ_LENGTH * sizeof(uint8_t));
                continue;
            }else if(MODBUS_GET_INT16_FROM_INT8(query, header_length + 1) 
                        == UT_REGISTERS_ADDRESS_SLEEP_500_MS){
                printf("Sleep 0.5 s before replying\n");
                usleep(500000);
            }else if (MODBUS_GET_INT16_FROM_INT8(query, header_length + 1) ==
                        == UT_REGISTERS_ADDRESS_SLEEP_5_MS){
                uint8_t req[] = "\x00\x1C\x00\x00\x00\x05\xFF\x03\x02\x00\x00";
                int req_length = 11;
                int w_s = modbus_get_socket(ctx);
                if (w_s == -1){
                    fprintf(stderr, "Unable to get valid socket in tst\n");
                    continue;
                }
                req[1] = query[1];
                for (i = 0; i < req_length; i++){
                    printf("%.2X", req[i]);
                    usleep(5000);
                    rc = send(w_s, (const char *) (req + i), 1, MSG_NOSIGNAL);
                    if (rc == -1){
                        break;
                    }
                }
                continue;
        }
    }
        rc = modbus_reply(ctx, query, rc, mb_mapping);
        if (rc == -1){
            break;
        }
    }
     printf("Quit the loop: %s\n", modbus_strerror(errno));

    if (use_backend == TCP) {
        if (s != -1) {
            close(s);
        }
    }
    modbus_mapping_free(mb_mapping);
    free(query);
    /* For RTU */
    modbus_close(ctx);
    modbus_free(ctx);


    return 0;
}

