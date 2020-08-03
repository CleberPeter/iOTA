#include "mqtt.h"

Mqtt::Mqtt()
{
    client = new QMqttClient(this);
    connect(client, &QMqttClient::stateChanged, this, &Mqtt::stateChange);
}


void Mqtt::tryConnect(QString _hostname, int _port, callback _callbackOnConnect)
{
    client->setCleanSession(true);
    client->setHostname(_hostname);
    client->setPort(_port);

    this->callbackOnConnect = _callbackOnConnect;

    client->connectToHost();
}

void Mqtt::stateChange(void)
{
    switch ((connectionSm) client->state())
    {
        case TRYING_CONNECT:
            qDebug() << "MQTT Trying Connection With Broker..." << endl;
        break;
        case CONNECTED:
            if (this->callbackOnConnect) this->callbackOnConnect(true);
            else {
                printf("Internal Error 0x00, Contact Mantainer!");
                exit(-1);
            }
        break;
        case DISCONNECTED:
            this->callbackOnConnect(false);
        break;
    }
}
