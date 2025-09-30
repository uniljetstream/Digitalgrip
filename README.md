# Digitalgrip - IoT 스위치 로봇

Arduino Nano IoT 33과 AWS Serverless Lambda를 활용한 대학교 졸업 프로젝트입니다.
Digitalgrip은 물리적 스위치를 원격으로 제어할 수 있는 IoT 스위치 로봇입니다.

## 📋 프로젝트 개요

- **하드웨어**: Arduino Nano IoT 33
- **클라우드**: AWS IoT Core, AWS Lambda
- **통신 프로토콜**: MQTT over TLS
- **주요 기능**:
  - 원격 스위치 제어 (On/Off)
  - 물리 버튼을 통한 로컬 제어
  - AWS IoT Device Shadow를 통한 상태 동기화
  - 서보모터를 이용한 물리적 스위치 조작

## 🗂️ 프로젝트 구조

```
Digitalgrip/
├── digitalgrip_main/
│   ├── digitalgrip_main.ino      # 메인 아두이노 스케치
│   ├── servo_motion.ino          # 서보모터 제어 함수
│   ├── networkconnect.ino        # WiFi 및 MQTT 연결 함수
│   └── messege.ino               # 메시지 수신/발신 처리
├── Lambda_Shadow_Status_Check.py # Device Shadow 상태 조회 Lambda
└── Lamda_Shadow_Update.py        # Device Shadow 업데이트 Lambda
```

## 🔧 하드웨어 구성

- **Arduino Nano IoT 33**: 메인 컨트롤러
- **서보모터**: 물리적 스위치 조작 (9번 핀 연결)
- **택트 스위치**: 로컬 제어용 버튼 (2번 핀 연결, 풀업 저항 사용)
- **ECC508 암호화 칩**: TLS 인증을 위한 보안 요소

## 💻 소프트웨어 구성

### Arduino 펌웨어

#### 주요 라이브러리
- `WiFiNINA`: WiFi 연결
- `ArduinoBearSSL`: TLS/SSL 암호화
- `ArduinoMqttClient`: MQTT 통신
- `ArduinoECCX08`: 하드웨어 보안 인증
- `ArduinoJson`: JSON 파싱
- `Servo`: 서보모터 제어

#### 동작 방식
1. WiFi 및 AWS IoT Core에 MQTT over TLS로 연결
2. SUBSCRIBE_TOPIC을 구독하여 원격 명령 수신
3. 로컬 버튼 또는 원격 명령으로 스위치 제어
4. 서보모터로 물리적 스위치 조작 (ON: 35도, OFF: 165도)
5. 상태 변경 시 PUBLISH_TOPIC으로 현재 상태 전송

### AWS Lambda 함수

#### 1. Lambda_Shadow_Status_Check.py
- **기능**: IoT Device Shadow 상태 조회
- **HTTP 메서드**: GET
- **파라미터**: `thingname` (쿼리 스트링)
- **반환**: 현재 스위치 상태 ("It's On" / "It's Off")

#### 2. Lamda_Shadow_Update.py
- **기능**: IoT Device Shadow 상태 업데이트
- **HTTP 메서드**: POST
- **파라미터**:
  - `thingname`: IoT Thing 이름
  - `action`: "on" 또는 "off"
- **동작**: Device Shadow의 desired 상태를 업데이트하여 디바이스에 명령 전달

## 🚀 설정 방법

### 1. Arduino 설정

1. `arduino_secrets.h` 파일 생성 및 아래 정보 입력:
```cpp
#define SECRET_SSID "your-wifi-ssid"
#define SECRET_PASS "your-wifi-password"
#define SECRET_BROKER "your-aws-iot-endpoint.iot.region.amazonaws.com"
#define SECRET_CERTIFICATE "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----\n"
```

2. AWS IoT Core에서 Thing 생성 및 인증서 발급
3. MQTT 토픽 설정:
   - PUBLISH_TOPIC: 디바이스에서 상태 전송용
   - SUBSCRIBE_TOPIC: 디바이스가 명령 수신용

4. Arduino IDE에서 펌웨어 업로드

### 2. AWS Lambda 설정

1. AWS Lambda 콘솔에서 Python 3.x 런타임으로 함수 생성
2. IAM 역할에 `iot:GetThingShadow`, `iot:UpdateThingShadow` 권한 부여
3. API Gateway와 연동하여 RESTful API 엔드포인트 생성
4. CORS 설정 (Origin: `*`)

## 📡 통신 프로토콜

### MQTT 메시지 포맷

**상태 보고 (Arduino → AWS):**
```json
{
  "state": {
    "reported": {
      "status": "on"  // or "off"
    }
  }
}
```

**명령 수신 (AWS → Arduino):**
```json
{
  "state": {
    "status": "on"  // or "off"
  }
}
```

## 🔐 보안

- TLS 1.2 암호화 통신
- ECC508 하드웨어 보안 칩을 통한 인증서 관리
- AWS IoT Core 정책을 통한 접근 제어

## 📝 라이선스

이 프로젝트는 대학교 졸업 프로젝트로 제작되었습니다.

## 👤 작성자

졸업 프로젝트 - Arduino Nano IoT 33 & AWS Serverless 기반 IoT 스위치 로봇
