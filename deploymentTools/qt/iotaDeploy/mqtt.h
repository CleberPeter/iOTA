#ifndef MQTT_H
#define MQTT_H

#include <QtMqtt/QMqttClient>

typedef void (*callback)(bool);

class Mqtt: public QObject
{
    Q_OBJECT
public:
    Mqtt();
    void tryConnect(QString _hostname, int _port, callback _callbackOnConnect);
    void tryPublish(QString topicName, QByteArray msg, int qos);

    QMqttClient *client;

private:

    QString hostname;
    int port;
    callback callbackOnConnect;

    typedef enum {

        DISCONNECTED = 0,
        TRYING_CONNECT,
        CONNECTED,

    }connectionSm;



private slots:
    void stateChange();

};

#endif // MQTT_H
