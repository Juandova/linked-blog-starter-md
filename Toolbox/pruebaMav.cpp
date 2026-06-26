#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <map>
#include <chrono>

std::map<uint8_t, int> msg_count;
std::map<uint8_t, std::chrono::steady_clock::time_point> msg_time;

extern "C" {
    #include "mavlink/generated/common/mavlink.h"
}

// ===================== UART SETUP =====================
int open_port(const char* port)
{
    int fd = open(port, O_RDWR | O_NOCTTY);

    if (fd < 0)
    {
        perror("Error abriendo puerto");
        return -1;
    }

    struct termios tty{};
    tcgetattr(fd, &tty);

    cfsetispeed(&tty, B57600);
    cfsetospeed(&tty, B57600);

    tty.c_cflag |= (CLOCAL | CREAD);
    tty.c_cflag &= ~PARENB;
    tty.c_cflag &= ~CSTOPB;
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;

    tty.c_lflag = 0;
    tty.c_iflag = 0;
    tty.c_oflag = 0;

    tcsetattr(fd, TCSANOW, &tty);

    return fd;
}

// ===================== MAVLINK NAME =====================
const char* mavlink_msg_name(uint8_t msgid)
{
    switch(msgid)
    {
        case MAVLINK_MSG_ID_HEARTBEAT: return "HEARTBEAT";
        case MAVLINK_MSG_ID_GPS_RAW_INT: return "GPS_RAW_INT";
        case MAVLINK_MSG_ID_GLOBAL_POSITION_INT: return "GLOBAL_POSITION_INT";
        case MAVLINK_MSG_ID_ATTITUDE: return "ATTITUDE";
        case MAVLINK_MSG_ID_VFR_HUD: return "VFR_HUD";
        case MAVLINK_MSG_ID_STATUSTEXT: return "STATUSTEXT";
        case MAVLINK_MSG_ID_SYS_STATUS: return "SYS_STATUS";
        default: return "UNKNOWN";
    }
}

// ===================== MAIN =====================
int main()
{
    const char* port = "/dev/ttyUSB0";
    int fd = open_port(port);

    if (fd < 0)
        return 1;

    std::cout << "Esperando MAVLink..." << std::endl;

    mavlink_message_t msg;
    mavlink_status_t status;

    uint8_t byte;

    // ====== Hz tracking ======
    std::map<uint8_t, int> count;
    std::map<uint8_t, std::chrono::steady_clock::time_point> start_time;

    while (true)
    {
        int n = read(fd, &byte, 1);

        if (n > 0)
        {
            if (mavlink_parse_char(MAVLINK_COMM_0, byte, &msg, &status))
            {
                uint8_t id = msg.msgid;

                // init timing
                if (start_time.find(id) == start_time.end())
                {
                    start_time[id] = std::chrono::steady_clock::now();
                    count[id] = 0;
                }

                count[id]++;

                // compute frequency every 1 second
                auto now = std::chrono::steady_clock::now();
                double elapsed = std::chrono::duration<double>(now - start_time[id]).count();

                if (elapsed >= 1.0)
                {
                    double hz = count[id] / elapsed;

                    std::cout
                        << "[" << (int)id << " "
                        << mavlink_msg_name(id) << "] "
                        << hz << " Hz"
                        << std::endl;

                    count[id] = 0;
                    start_time[id] = now;
                }

                // ===== OPTIONAL DECODING =====
                if (id == MAVLINK_MSG_ID_GPS_RAW_INT)
                {
                    mavlink_gps_raw_int_t gps;
                    mavlink_msg_gps_raw_int_decode(&msg, &gps);
                }

                if (id == MAVLINK_MSG_ID_ATTITUDE)
                {
                    mavlink_attitude_t att;
                    mavlink_msg_attitude_decode(&msg, &att);
                }

                if (id == MAVLINK_MSG_ID_GLOBAL_POSITION_INT)
                {
                    mavlink_global_position_int_t pos;
                    mavlink_msg_global_position_int_decode(&msg, &pos);
                }
            }
        }
    }

    close(fd);
    return 0;
}