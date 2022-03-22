# 수도권 버스 정류장 / 수도권 버스 도착 안내

아래에는 서울, 경기, 인천 지역의 버스 정류소 및 버스 도착 안내에 대하여 서술되어 있습니다.

### /station

정류장 정보를 불러옵니다.

```
https://api.yhs.kr/bus/station
```

#### Parameter

<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>형태</th>
        <th>필수 유무</th>
        <th>기본 값</th>
        <th>비고</th>
    </tr>
    <tr>
        <th>name</th>
        <td>정류소 명칭</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>cityCode</th>
        <td>도시 코드</td>
        <td>integer</td>
        <td>X</td>
        <td>1</td>
        <td>
            1: 자동 설정<br/>
            11: 서울 지역<br/>
            12: 경기 지역<br/>
            13: 인천 지역<br/>
        </td>
    </tr>
</table>

#### Return

```json
[
  {
    "displayId": 22009,
    "id": 22009,
    "name": "신분당선강남역",
    "posX": 127.0284005454,
    "posY": 37.4960417459,
    "stationId": 121000009,
    "type": 11
  }
]
```

* 기본 구조

<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>형태</th>
        <th>필수 유무</th>
        <th>기본 값</th>
        <th>비고</th>
    </tr>
    <tr>
        <th>displayId</th>
        <td>정류장 ID(사용자)</td>
        <td>integer</td>
        <td>X</td>
        <td></td>
        <td>수도권 정류장 ID(5자리)</td>
    </tr>
    <tr>
        <th>id</th>
        <td>정류장 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td>도착정보 조회를 위한 ID값</td>
    </tr>
    <tr>
        <th>name</th>
        <td>정류장 명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>posX</th>
        <td>정류장 X좌표</td>
        <td>float</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>posY</th>
        <td>정류장 Y좌표</td>
        <td>float</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>stationId</th>
        <td>정류장 ID(개발자)</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>type</th>
        <td>출처</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td>
            도착정보 조회를 위한 유형<br/>
            1: 자동 설정(/route 용)<br/>
            2: 자동 설정(버스정류소 검색용)<br/>
            11: 서울 지역<br/>
            12: 경기 지역<br/>
            13: 인천 지역<br/>
        </td>
    </tr>
</table>

### /station/around

좌표 값을 기준으로 주변에 있는 정류장 정보를 불러옵니다.

```
https://api.yhs.kr/bus/station/around
```

#### Parameter

<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>형태</th>
        <th>필수 유무</th>
        <th>기본 값</th>
        <th>비고</th>
    </tr>
    <tr>
        <th>posX</th>
        <td>경도</td>
        <td>float</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>posY</th>
        <td>위도</td>
        <td>float</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>cityCode</th>
        <td>도시 코드</td>
        <td>integer</td>
        <td>X</td>
        <td>1</td>
        <td>
            1: 자동 설정<br/>
            11: 서울 지역<br/>
            12: 경기 지역<br/>
            13: 인천 지역<br/>
        </td>
    </tr>
</table>

#### Return

```json
[
  {
    "distance": 100,
    "displayId": 22009,
    "id": 22009,
    "name": "신분당선강남역",
    "posX": 127.0284005454,
    "posY": 37.4960417459,
    "stationId": 121000009,
    "type": 11
  }
]
```

* 기본 구조

<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>형태</th>
        <th>필수 유무</th>
        <th>기본 값</th>
        <th>비고</th>
    </tr>
    <tr>
        <th>displayId</th>
        <td>정류장 ID(사용자)</td>
        <td>integer</td>
        <td>X</td>
        <td></td>
        <td>수도권 정류장 ID(5자리)</td>
    </tr>
    <tr>
        <th>distance</th>
        <td>정류장까지 거리</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td>m(미터법) 기준</td>
    </tr>
    <tr>
        <th>id</th>
        <td>정류장 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td>도착정보 조회를 위한 ID값</td>
    </tr>
    <tr>
        <th>name</th>
        <td>정류장 명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>posX</th>
        <td>정류장 X좌표</td>
        <td>float</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>posY</th>
        <td>정류장 Y좌표</td>
        <td>float</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>stationId</th>
        <td>정류장 ID(개발자)</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>type</th>
        <td>출처</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td>
            도착정보 조회를 위한 유형<br/>
            1: 자동 설정<br/>
            11: 서울 지역<br/>
            12: 경기 지역<br/>
            13: 인천 지역<br/>
        </td>
    </tr>
</table>

### /route

정류장 내 버스 도착 정보를 불러옵니다.

```
https://api.yhs.kr/bus/route
```

#### Parameter

<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>형태</th>
        <th>필수 유무</th>
        <th>기본 값</th>
        <th>비고</th>
    </tr>
    <tr>
        <th>id</th>
        <td>정류소 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td><code>/station</code>에서 구한 <code>id</code>값</td>
    </tr>
    <tr>
        <th>cityCode</th>
        <td>도시 코드</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td>
            <code>/station</code>에서 구한 <code>type</code>값<br/>
            11: 서울 지역<br/>
            12: 경기 지역<br/>
            13: 인천 지역<br/>
        </td>
    </tr>
</table>

#### Return

```json
[
    {
        "arrivalInfo":[
            {
                "carNumber": null,
                "congestion": null,
                "isArrival": false,
                "isFull": false,
                "lowBus": true,
                "prevCount": 5,
                "seat": null,
                "time": 436
            }
        ],
        "id": "100100409",
        "name": "421",
        "type":"1003"
    }
]
```

* **기본 구조**
<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>형태</th>
        <th>필수 유무</th>
        <th>기본 값</th>
        <th>비고</th>
    </tr>
    <tr>
        <th>arrivalInfo</th>
        <td>도착 정보</td>
        <td>List[ArrivalInfo]</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>id</th>
        <td>경로 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>name</th>
        <td>노선명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>type</th>
        <td>노선유형</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td>아래 노선 유형 참고</td>
    </tr>
</table>

* **ArrivalInfo 구조**<br/>
△는 평상시에는 필수 적으로 반환되다가, 운영이 종료되거나, 정보를 조회할 수 없을 때 `null` 혹은 기본 값을 반환합니다.
<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>형태</th>
        <th>필수 유무</th>
        <th>기본 값</th>
        <th>비고</th>
    </tr>
    <tr>
        <th>carNumber</th>
        <td>차량 번호</td>
        <td>string</td>
        <td>X</td>
        <td>null</td>
        <td></td>
    </tr>
    <tr>
        <th>congestion</th>
        <td>혼잡도</td>
        <td>integer</td>
        <td>X</td>
        <td>null</td>
        <td>
            1: 여유<br/>
            2: 보통<br/>
            3: 혼잡<br/>
        </td>
    </tr>
    <tr>
        <th>isArrival</th>
        <td>(곧)도착 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td>false</td>
        <td></td>
    </tr>
    <tr>
        <th>isFull</th>
        <td>만차 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td>false</td>
        <td></td>
    </tr>
    <tr>
        <th>lowBus</th>
        <td>저상 버스 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td>false</td>
        <td></td>
    </tr>
    <tr>
        <th>prevCount</th>
        <td>차량 위치 정보(N 번째 전 정류소)</td>
        <td>integer</td>
        <td>△</td>
        <td>null</td>
        <td></td>
    </tr>
    <tr>
        <th>seat</th>
        <td>빈 자릿수</td>
        <td>integer</td>
        <td>X</td>
        <td>null</td>
        <td></td>
    </tr>
    <tr>
        <th>time</th>
        <td>예상 도착 시간</td>
        <td>integer</td>
        <td>△</td>
        <td>null</td>
        <td>초 단위</td>
    </tr>
</table>

* **노선 유형**
<table>
    <tr>
        <th>키</th>
        <th>설명</th>
        <th>지역</th>
    </tr>
    <tr>
        <th>1001</th>
        <td><img src="https://via.placeholder.com/15/8b4513/000?text=+"> 공항버스</td>
        <td rowspan="8">서울</td>
    </tr>
    <tr>
        <th>1002</th>
        <td><img src="https://via.placeholder.com/15/5bb025/000?text=+"> 마을버스</td>
    </tr>
    <tr>
        <th>1003</th>
        <td><img src="https://via.placeholder.com/15/3d5bab/000?text=+"> 간선버스</td>
    </tr>
    <tr>
        <th>1004</th>
        <td><img src="https://via.placeholder.com/15/5bb025/000?text=+"> 지선버스</td>
    </tr>
    <tr>
        <th>1005</th>
        <td><img src="https://via.placeholder.com/15/f99d1c/000?text=+"> 순환버스</td>
    </tr>
    <tr>
        <th>1006</th>
        <td><img src="https://via.placeholder.com/15/F72f08/000?text=+"> 광역버스</td>
    </tr>
    <tr>
        <th>1009</th>
        <td>페지노선</td>
    </tr>
    <tr>
        <th>1000</th>
        <td>공용버스</td>
    </tr>
    <tr>
        <th>2011</th>
        <td><img src="https://via.placeholder.com/15/FF0000/000?text=+"> 직행좌석 시내버스</td>
        <td rowspan="16">경기</td>
    </tr>
    <tr>
        <th>2012</th>
        <td><img src="https://via.placeholder.com/15/0075C8/000?text=+"> 좌석 시내버스</td>
    </tr>
    <tr>
        <th>2013</th>
        <td><img src="https://via.placeholder.com/15/33CC99/000?text=+"> 일반 시내버스</td>
    </tr>
    <tr>
        <th>2014</th>
        <td><img src="https://via.placeholder.com/15/000000/000?text=+"> 광역급행 시내버스</td>
    </tr>
    <tr>
        <th>2015</th>
        <td><img src="https://via.placeholder.com/15/B62367/000?text=+"> 맞춤형버스(舊 따복버스)</td>
    </tr>
    <tr>
        <th>2016</th>
        <td><img src="https://via.placeholder.com/15/FF0000/000?text=+"> 경기순환버스</td>
    </tr>
    <tr>
        <th>2021</th>
        <td><img src="https://via.placeholder.com/15/FF0000/000?text=+"> 직행좌석 농어촌버스</td>
    </tr>
    <tr>
        <th>2022</th>
        <td><img src="https://via.placeholder.com/15/0075C8/000?text=+"> 좌석 농어촌버스</td>
    </tr>
    <tr>
        <th>2023</th>
        <td><img src="https://via.placeholder.com/15/33CC99/000?text=+"> 일반 농어촌버스</td>
    </tr>
    <tr>
        <th>2030</th>
        <td><img src="https://via.placeholder.com/15/F99D1C/000?text=+"> 마을버스</td>
    </tr>
    <tr>
        <th>2041</th>
        <td>고속 시외버스</td>
    </tr>
    <tr>
        <th>2042</th>
        <td><img src="https://via.placeholder.com/15/0075C8/000?text=+"> 좌석 시외버스</td>
    </tr>
    <tr>
        <th>2043</th>
        <td><img src="https://via.placeholder.com/15/a800ff/000?text=+"> 일반 시외버스</td>
    </tr>
    <tr>
        <th>2051</th>
        <td><img src="https://via.placeholder.com/15/aa9872/000?text=+"> 리무진 공항버스</td>
    </tr>
    <tr>
        <th>2052</th>
        <td><img src="https://via.placeholder.com/15/0075C8/000?text=+"> 좌석 공항버스</td>
    </tr>
    <tr>
        <th>2053</th>
        <td><img src="https://via.placeholder.com/15/8b4513/000?text=+"> 일반 공항버스</td>
    </tr>
    <tr>
        <th>3001</th>
        <td><img src="https://via.placeholder.com/15/5bb025/000?text=+"> 지선버스</td>
        <td rowspan="9">인천</td>
    </tr>
    <tr>
        <th>3002</th>
        <td><img src="https://via.placeholder.com/15/3366cc/000?text=+"> 간선버스</td>
    </tr>
    <tr>
        <th>3003</th>
        <td><img src="https://via.placeholder.com/15/3d5bab/000?text=+"> 좌석버스</td>
    </tr>
    <tr>
        <th>3004</th>
        <td><img src="https://via.placeholder.com/15/f72f08/000?text=+"> 광역버스</td>
    </tr>
    <tr>
        <th>3005</th>
        <td>리무진 버스</td>
    </tr>
    <tr>
        <th>3006</th>
        <td><img src="https://via.placeholder.com/15/5bb025/000?text=+"> 마을버스</td>
    </tr>
    <tr>
        <th>3007</th>
        <td>순환버스</td>
    </tr>
    <tr>
        <th>3008</th>
        <td><img src="https://via.placeholder.com/15/000/000?text=+"> 급행간선버스</td>
    </tr>
    <tr>
        <th>3009</th>
        <td><img src="https://via.placeholder.com/15/5bb025/000?text=+"> 지선순환버스</td>
    </tr>
</table>
