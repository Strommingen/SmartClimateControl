import ubinascii, time
import library.mqtt

# Callback Function to respond to messages from Adafruit IO
def sub_cb(topic, msg) -> None:          # sub_cb means "callback subroutine"
    print((topic, msg))          # Outputs the message that was received. Debugging use.
    # if msg == b"ON":             # If message says "ON" ...
    #     led.on()                 # ... then LED on
    # elif msg == b"OFF":          # If message says "OFF" ...
    #     led.off()                # ... then LED off
    # else:                        # If any other message is received ...
    print("Unknown message") # ... do nothing but output that it happened.

class AdaWebhook:

    def __init__(self, topic, client) -> None:
        self._topic = topic
        self._client = client
        self.RANDOMS_INTERVAL = 60000    # milliseconds
        self.last_random_sent_ticks = 0  # milliseconds


    def publish(self, data, isNotified) -> None:
        if(((time.ticks_ms() - self.last_random_sent_ticks) < self.RANDOMS_INTERVAL) and not
        isNotified):
            return
        
        print(f"Publishing: {data} to {self._topic}")
        try:
            self._client.publish(topic=self._topic, msg=str(data))
            print("DONE")
        except Exception as err:
            print("FAILED")
        finally:
            self.last_random_sent_ticks = time.ticks_ms()
