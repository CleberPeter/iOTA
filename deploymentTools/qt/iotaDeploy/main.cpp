#include <QCoreApplication>
#include <string.h>
#include "mqtt.h"
#include "util.h"

struct
{
    QString uuid;
    QString file;
    QString host;
    int version;
    int sizeBlocks;
    int port;
} parametersToDeploy;

Mqtt mqtt;

void printTip(void)
{
    qDebug("\n\nRun by passing parameters like:\n\n./iotaDeploy -u 1 -f firmware.bin -v 711 -sb 256 -h 192.168.0.4 -p 1883 \n\n");
}

bool intToStr(char* str, int *ret)
{
    char *dummyPtr;

    *ret = strtol(str, &dummyPtr, 10);
    if (*dummyPtr) return false; // failed conversion ...

    return true;
}

bool parseParameters(int argc, char *argv[])
{
    if (argc == 13)
    {
        qDebug("Parsing Parameters ...\n\n");
        for (int i=1; i < argc; i++) // ignore first parameter
        {
            if (!strcmp(argv[i], "-u"))
            {
                qDebug("uuid: %s\n", argv[++i]);
                parametersToDeploy.uuid = argv[i];
            }
            else if (!strcmp(argv[i], "-f"))
            {
                qDebug("file: %s\n", argv[++i]);
                parametersToDeploy.file = argv[i];
            }
            else if (!strcmp(argv[i], "-v"))
            {
                qDebug("version: %s\n", argv[++i]);

                if (!intToStr(argv[i], &parametersToDeploy.version)) // failed conversion ...
                {
                    qDebug("\nError! Version Invalid.");
                    return false;
                }
            }
            else if (!strcmp(argv[i], "-sb"))
            {
                qDebug("block size: %s\n", argv[++i]);

                if (!intToStr(argv[i], &parametersToDeploy.sizeBlocks)) // failed conversion ...
                {
                    qDebug("\nError! Size Blocks Invalid.");
                    return false;
                }
            }
            else if (!strcmp(argv[i], "-h"))
            {
                qDebug("broker host: %s\n", argv[++i]);
                parametersToDeploy.host = argv[i];
            }
            else if (!strcmp(argv[i], "-p"))
            {
                qDebug("broker port: %s\n", argv[++i]);
                if (!intToStr(argv[i], &parametersToDeploy.port)) // failed conversion ...
                {
                    qDebug("\nError! Port Invalid.");
                    return false;
                }
            }
            else
            {
                qDebug("Error! Wrong Parameter.\n");
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

    pFile = fopen(parametersToDeploy.file.toLocal8Bit().data() , "rb" );

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

    // fread(buffer, 1, 50, pFile); // remove header

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

bool deployVersion()
{
    QString topic = "iota/" + parametersToDeploy.uuid + "/metadata";
    QString msg = "{\"version\":" + QString::number(parametersToDeploy.version) + ",\"size\":" + QString::number(parametersToDeploy.sizeBlocks) + "}";
    QByteArray buff_arr = msg.toUtf8();

    if (mqtt.client->publish(topic, buff_arr, 2, true) == -1)
    {
        qDebug("Could not publish message\n");
        return false;
    }

    return true;
}

bool deployUpdate(void)
{
    if (deployVersion())
    {
        //if (deployFirmware())
        {
            return true;
        }
    }

    return false;
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
