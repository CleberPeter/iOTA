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
    int port;
    int sizeBlocks = 0;
    int incrementalNumber = -1;
    QString dateExpiration = "";
    bool splitInBlocks = false;
} parametersToDeploy;

Mqtt mqtt;

void printTip(void)
{
    qDebug("\n\nRun by passing parameters like:\n\n./iotaDeploy -u 1 -f firmware -v 800 -sb 512 -h localhost -p 1883 -split -d 2021-05-06 -n 11 \n\n");
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
    if (argc > 14)
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
            else if (!strcmp(argv[i], "-split")) parametersToDeploy.splitInBlocks = true;
            else if (!strcmp(argv[i], "-d"))
            {
                qDebug("dateExpiration: %s\n", argv[++i]);
                parametersToDeploy.dateExpiration = argv[i];
            }
            else if (!strcmp(argv[i], "-n"))
            {
                qDebug("incremental number: %s\n", argv[++i]);

                if (!intToStr(argv[i], &parametersToDeploy.incrementalNumber)) // failed conversion ...
                {
                    qDebug("\nError! Incremental Number Invalid.");
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
            else
            {
                qDebug("Error! Wrong Parameter.\n");
                return false;
            }
        }

        if (parametersToDeploy.incrementalNumber == -1)
        {
            qDebug("Error! Missing incremental number.\n");
            return false;
        }
        else if (parametersToDeploy.dateExpiration == "")
        {
            qDebug("Error! Missing date expiration.\n");
            return false;
        }
        else if (parametersToDeploy.splitInBlocks && !parametersToDeploy.sizeBlocks)
        {
            qDebug("Error! Missing the size of the blocks.\n");
            return false;
        }
        else return true;
    }

    printf("Error! Missing Parameters.\n");
    return false;
}

int deployFirmware(void)
{
    FILE * pFile;
    QByteArray buff_arr;
    QString topic;
    int pckgCounter = 0;

    pFile = fopen(parametersToDeploy.file.toLocal8Bit().data() , "rb" );

    if (pFile==NULL)
    {
        qDebug("Error. Can't Open Binary File\n");
        return 0;
    }

    fseek(pFile, 0L, SEEK_END);
    int fileSize = ftell(pFile);

    qDebug("\nFile Size: %d\n", fileSize);

    fseek(pFile, 0L, SEEK_SET);

    qDebug("\nDeploying ...\n");

    int bytesReaded = 0;

    if (parametersToDeploy.splitInBlocks)
    {
        char buffer[parametersToDeploy.sizeBlocks];

        while(true)
        {
            bytesReaded = fread(buffer, 1, parametersToDeploy.sizeBlocks, pFile);

            if (bytesReaded > 0)
            {
                buff_arr = QByteArray::fromRawData(buffer, parametersToDeploy.sizeBlocks);

                if (bytesReaded < parametersToDeploy.sizeBlocks)
                {
                    for (int i = bytesReaded; i < parametersToDeploy.sizeBlocks; i++) buff_arr[i] = 0xFF;

                    qDebug() << buff_arr;
                }

                topic = "iota/"+parametersToDeploy.uuid+"/firmware/block/"+ QString::number(pckgCounter);

                if (mqtt.client->publish(topic, buff_arr, 2, true) == -1)
                {
                    qDebug("Could not publish message\n");
                    return 0;
                }

                pckgCounter++;

                if (bytesReaded < parametersToDeploy.sizeBlocks) break;
            }
            else break;
        }
    }
    else
    {
        char buffer[fileSize];
        bytesReaded = fread(buffer, 1, fileSize, pFile);

        if (bytesReaded != fileSize)
        {
            qDebug("Error. Can't Read Binary File\n");
            return 0;
        }
        else
        {
            buff_arr = QByteArray::fromRawData(buffer, fileSize);
            topic = "iota/"+parametersToDeploy.uuid+"/firmware";

            if (mqtt.client->publish(topic, buff_arr, 2, true) == -1)
            {
                qDebug("Could not publish message\n");
                return 0;
            }
            else pckgCounter = 2;
        }
    }


    pckgCounter--;

    if (bytesReaded) qDebug() << "\nPublished:" << pckgCounter-1 << "blocks of" << parametersToDeploy.sizeBlocks << "bytes + 1 block of" << bytesReaded << "bytes." << endl;
    else qDebug() << "\nPublished:" << pckgCounter << "blocks of" << parametersToDeploy.sizeBlocks << "bytes." << endl;

    fclose(pFile);

    return pckgCounter;
}

bool deployVersion(int qtyBlocks)
{
    QString topic = "iota/" + parametersToDeploy.uuid + "/manifest";
    QString msg = "{\"version\":" + QString::number(parametersToDeploy.version) + ",\"dateExpiration\":" + parametersToDeploy.dateExpiration + ",\"incrementalNumber\":" + QString::number(parametersToDeploy.incrementalNumber) + ",\"sizeOfBlocks\":" + QString::number(parametersToDeploy.sizeBlocks) + ",\"numberOfBlocks\":" + QString::number(qtyBlocks) + "}";
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
    int qtyBlocks = deployFirmware();
    if (qtyBlocks && deployVersion(qtyBlocks)) return true;
    else return false;
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
