WiFiClient *stream = http.getStreamPtr();

while (http.connected()) {
  int len = stream->available();
  if (len) {
    uint8_t buf[64];
    int r = stream->readBytes(buf, 64);

    Serial.print("BYTES: ");
    Serial.println(r);

    // első pár byte kiírás
    for (int i = 0; i < 16; i++) {
      Serial.print(buf[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    size_t out;
    i2s_write(I2S_NUM_0, buf, r, &out, portMAX_DELAY);
  }
}
