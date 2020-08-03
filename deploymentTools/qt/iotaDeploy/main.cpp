#include <QCoreApplication>
#include <string.h>
#include "mqtt.h"
#include "util.h"

struct
{
    char *device;
    char *file;
    char *host;
    int version;
    int sizeBlocks;
    int port;
} parametersToDeploy;

Mqtt mqtt;

void printTip(void)
{
    printf("\n\nRun by passing parameters like:\n\n./companytecDeploy -d HRS -f firmware.bin -v 711 -sb 256 -h 192.168.0.4 -p 1883 \n\n");
}

bool intToStr(char* str, int *ret)
{
    char *dummyPtr;

    *ret = strtol(str, &dummyPtr, 10);
    if (*dummyPtr) return false; // failed conversion ...

    return true;
}

// ./companytecDeploy -d HRS -f firmware.bin -v 711 -sb 256 -h 192.168.0.4 -p 1883
bool parseParameters(int argc, char *argv[])
{
    if (argc == 13)
    {
        printf("Parsing Parameters ...\n\n");
        for (int i=1; i < argc; i++) // ignore first parameter
        {
            if (!strcmp(argv[i], "-d"))
            {
                printf("device: %s\n", argv[++i]);
                parametersToDeploy.device = argv[i];
            }
            else if (!strcmp(argv[i], "-f"))
            {
                printf("file: %s\n", argv[++i]);
                parametersToDeploy.file = argv[i];
            }
            else if (!strcmp(argv[i], "-v"))
            {
                printf("version: %s\n", argv[++i]);

                if (!intToStr(argv[i], &parametersToDeploy.version)) // failed conversion ...
                {
                    printf("\nError! Version Invalid.");
                    return false;
                }
            }
            else if (!strcmp(argv[i], "-sb"))
            {
                printf("block size: %s\n", argv[++i]);

                if (!intToStr(argv[i], &parametersToDeploy.sizeBlocks)) // failed conversion ...
                {
                    printf("\nError! Size Blocks Invalid.");
                    return false;
                }
            }
            else if (!strcmp(argv[i], "-h"))
            {
                printf("broker host: %s\n", argv[++i]);
                parametersToDeploy.host = argv[i];
            }
            else if (!strcmp(argv[i], "-p"))
            {
                printf("broker port: %s\n", argv[++i]);
                if (!intToStr(argv[i], &parametersToDeploy.port)) // failed conversion ...
                {
                    printf("\nError! Port Invalid.");
                    return false;
                }
            }
            else
            {
                printf("Error! Wrong Parameter.\n");
                return false;
            }
        }

        return true;
    }

    printf("Error! Missing Parameters.\n");
    return false;
}


int deployFirmware(void)
{
    FILE * pFile;
    QByteArray buff_arr;
    char buffer[parametersToDeploy.sizeBlocks];
    QString topic;
    int pckgCounter = 0;

    pFile = fopen (parametersToDeploy.file , "rb" );

    fseek(pFile, 0L, SEEK_END);
    int sz = ftell(pFile);

    printf("\nFile Size: %d\n", sz);

    fseek(pFile, 0L, SEEK_SET);

    if (pFile==NULL)
    {
        printf("Error. Can't Open Binary File\n");
        return 0;
    }

    printf("\nDeploying ...\n");

    int bytesReaded = 0;

    fread(buffer, 1, 50, pFile); // remove header

    while(true)
    {
        bytesReaded = fread(buffer, 1, parametersToDeploy.sizeBlocks, pFile);
        // printf("\nReaded %d Bytes\n", bytesReaded);

        if (bytesReaded > 0)
        {
            buff_arr = QByteArray::fromRawData(buffer, parametersToDeploy.sizeBlocks);

            if (bytesReaded < parametersToDeploy.sizeBlocks)
            {
                for (int i = bytesReaded; i < parametersToDeploy.sizeBlocks; i++) buff_arr[i] = 0xFF;

                qDebug() << buff_arr;
            }

            /*topic = "HRS/V2/"+QString::number(parametersToDeploy.version)+"/"+ QString::number(int(pckgCounter/10)) +"/" + QString::number(pckgCounter%10);
            if (mqtt.client->publish(topic, buff_arr, 2, true) == -1)
            {
                printf("Could not publish message\n");
                return 0;
            }*/

            //if (pckgCounter != 100)
            {
                topic = "HRS/Vrs/1/"+ QString::number(pckgCounter);

                // topic = "HRS/Version/"+QString::number(parametersToDeploy.version)+"/"+ QString::number(pckgCounter);

                if (mqtt.client->publish(topic, buff_arr, 2, true) == -1)
                {
                    printf("Could not publish message\n");
                    return 0;
                }
            }

            pckgCounter++;

            if (bytesReaded < parametersToDeploy.sizeBlocks) break;
        }
        else break;
    }

    pckgCounter--;

    if (bytesReaded) qDebug() << "\nPublished:" << pckgCounter << "blocks of" << parametersToDeploy.sizeBlocks << "bytes + 1 block of" << bytesReaded << "bytes." << endl;
    else qDebug() << "\nPublished:" << pckgCounter << "blocks of" << parametersToDeploy.sizeBlocks << "bytes." << endl;

    fclose(pFile);

    return pckgCounter;
}

bool deployVersion(int qty_blocks)
{
    QString topic = "HRS/QueryVersion/1";
    QString msg = "{\"version\":" + QString::number(parametersToDeploy.version) + ",\"size\":" + QString::number(qty_blocks) + "}";
    QByteArray buff_arr = msg.toUtf8();

    if (mqtt.client->publish(topic, buff_arr, 2, true) == -1)
    {
        printf("Could not publish message\n");
        return false;
    }

    return true;
}

bool deployUpdate(void)
{
    for (int i=10000; i < 10005; i++)
    {
        qDebug() << i;

        QString topic = "HRS/ConsoleData/" + QString::number(i);

        int sec = i%25;
        if (!sec) sec = 1;

        QString msg = "{\"DT\":\"2020-07-"+QString::number(sec)+" 08:27:47\",\"Mac\":\""+QString::number(i)+"\",\"MqttVersion\":\""+QString::number(i)+"\",\"HrsVersion\":"+QString::number(20000)+",\"CountSale\":"+QString::number(i)+",\"CountReserv\":"+QString::number(i)+"}";

        QByteArray buff_arr = msg.toUtf8();

        if (mqtt.client->publish(topic, buff_arr, 0, true) == -1)
        {
            printf("Could not publish message\n");
            return false;
        }
    }

    return true;
}

void mqttConnected(bool connected)
{
    if (connected)
    {
        printf("Connected! \n");


        if (!deployUpdate()) exit(-1);
        else printf("Success! Firmware Deployed.\n");
    }
    else
    {
        printf("Disconnected! \n");
        Util::sleep(3e3); // wait to try again
        mqtt.tryConnect(parametersToDeploy.host, parametersToDeploy.port, mqttConnected);
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    if (parseParameters(argc, argv))
    {
        printf("\nSuccess! All Parameters Parsed.\n\n");
        mqtt.tryConnect(parametersToDeploy.host, parametersToDeploy.port, mqttConnected);

        return a.exec();
    }
    else printTip();

    return -1;
}
