# 수도권 지하철 역사 / 도착정보 / 시간표 안내

아래에는 수도권 지역의 지하철/전철 역사 정보, 시간표 및 실시간 도착 정보에 대하여 서술되어 있습니다.

### 객체
아래의 객체는 해당 API에 주로 사용되는 공통 객체 입니다.
#### MetroStationInfo

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
        <th>arrivalStationId</th>
        <td>실시간 도착 정보 역ID</td>
        <td>integer</td>
        <td>X</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>code</th>
        <td>외부 코드(역코드)</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>displayName</th>
        <td>취급 역명</td>
        <td>string</td>
        <td>X</td>
        <td></td>
        <td>운영사에서 취급하는 역사명</td>
    </tr>
    <tr>
        <th>id</th>
        <td>역사 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td>시간표용 ID값</td>
    </tr>
    <tr>
        <th>name</th>
        <td>역사명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td><a href="#/around">/around</a>에서 미제공</td>
    </tr>
    <tr>
        <th>posX</th>
        <td>경도</td>
        <td>float</td>
        <td>X</td>
        <td></td>
        <td><a href="#/around">/around</a>에서 미제공</td>
    </tr>
    <tr>
        <th>posY</th>
        <td>위도</td>
        <td>float</td>
        <td>X</td>
        <td></td>
        <td><a href="#/around">/around</a>에서 미제공</td>
    </tr>
    <tr>
        <th>subway</th>
        <td>노선명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>subwayId</th>
        <td>노선 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

#### ArrivalInfo

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
        <th>destination</th>
        <td>목적지</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>direction</th>
        <td>방향</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>direction_name</th>
        <td>방향(이름)</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>heading</th>
        <td>출입문</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>isArrive</th>
        <td>도착 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>isDeparture</th>
        <td>출발 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>isEntry</th>
        <td>진입 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>isPrevArrive</th>
        <td>전역 도착 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>isPrevDeparture</th>
        <td>전역 출발 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>isPrevEntry</th>
        <td>전역 진입 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>isRapid</th>
        <td>급행 유무</td>
        <td>boolean</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>nextStation</th>
        <td>다음역 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>prevCount</th>
        <td>남은 역 수(n역 전)</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>prevStation</th>
        <td>이전역 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>rapidInfo</th>
        <td>급행 열차 정보</td>
        <td>string</td>
        <td>X</td>
        <td>null</td>
        <td></td>
    </tr>
    <tr>
        <th>stationId</th>
        <td>이번역 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>subway</th>
        <td>지하철 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>time</th>
        <td>도착 시간</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>train</th>
        <td>열차 명(번호)</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>


### /station

전철역 정보를 불러옵니다.

```
https://api.yhs.kr/metro/station
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
        <td>전철/지하철 역사명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

#### Return

```json
[
  {
    "arrivalStationId": 1001000133,
    "code": "133",
    "displayName": "서울역",
    "id": "0150",
    "name": "서울역",
    "posX": 126.972559,
    "posY": 37.554648,
    "subway": "1호선",
    "subwayId": 1001
  }
]
```

* 기본 객체

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
        <th></th>
        <td>지하철 역사 정보</td>
        <td>list[<a href="#MetroStationInfo">MetroStationInfo</a>]</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

### /around

전철역 주변 정보를 불러옵니다.

```
https://api.yhs.kr/metro/around
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
        <th>distance</th>
        <td>반경</td>
        <td>integer</td>
        <td>X</td>
        <td>500</td>
        <td>미터법(m) 적용</td>
    </tr>
    <tr>
        <th>details</th>
        <td>자세한 정보</td>
        <td>boolean</td>
        <td>X</td>
        <td>True</td>
        <td></td>
    </tr>
</table>

#### Return

```json
{
  "서울역": {
    "data": [
      {
        "arrivalStationId": 1001000133,
        "code": "133",
        "displayName": "서울역",
        "id": "0150",
        "subway": "1호선",
        "subwayId": 1001
      }
    ],
    "direction": 0,
    "distance": 0.0,
    "posX": 126.972559,
    "posY": 37.554648
  }
}
```

* 기본 객체

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
        <th></th>
        <td>지하철 역사 정보</td>
        <td>union[string, AroundStationInfo]</td>
        <td>O</td>
        <td></td>
        <td>
            details 활성화: string<br/>
            details 비활성화: list[AroundStationInfo]
        </td>
    </tr>
</table>

* AroundStationInfo 객체

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
        <th>data</th>
        <td>지하철 역사 정보</td>
        <td><a href="#MetroStationInfo">MetroStationInfo</a></td>
        <td>O</td>
        <td></td>
        <td>/around 형태로 변환</td>
    </tr>
    <tr>
        <th>direction</th>
        <td>방향</td>
        <td>Integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>distance</th>
        <td>거리</td>
        <td>Integer</td>
        <td>O</td>
        <td></td>
        <td>미터법(m) 적용</td>
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
</table>

### /arrival

실시간 도착 정보를 불러옵니다.

```
https://api.yhs.kr/metro/arrival
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
        <td>전철/지하철 도착 정보 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

#### Return

```json
{
  "arrival": [
    {
      "destination": "군자(능동) (막차)",
      "direction": 0,
      "direction_name": "상행",
      "heading": "오른쪽",
      "isArrive": false,
      "isDeparture": false,
      "isEntry": false,
      "isPrevArrive": false,
      "isPrevDeparture": false,
      "isPrevEntry": false,
      "isRapid": false,
      "nextStation": "1005080549",
      "prevCount": 5,
      "prevStation": "1005080551",
      "rapidInfo": null,
      "stationId": "1005080550",
      "time": 960,
      "train": "5662"
    }
  ],
  "displayName": "올림픽공원(한국체대)",
  "stationId": 1005080550,
  "stationName": "올림픽공원",
  "subway": 1005,
  "transform": {
      "1009": {
          "arrival": [],
          "displayName": "올림픽공원",
          "stationId": 1009000936
      }
  }
}
```

* 기본 객체

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
        <th>arrival</th>
        <td>도착 정보</td>
        <td>list[<a href="#ArrivalInfo">ArrivalInfo</a>]</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>displayName</th>
        <td>취급 역명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td>운영사에서 취급하는 역사명</td>
    </tr>
    <tr>
        <th>stationId</th>
        <td>실시간 도착 정보 역ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>name</th>
        <td>역사명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
    </tr>
    <tr>
        <th>subway</th>
        <td>지하철 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>transform</th>
        <td>환승 정보</td>
        <td>json(string, TransformArrival 객체)</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

* TransformArrival 객체

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
        <th>arrival</th>
        <td>도착 정보</td>
        <td>list[<a href="#ArrivalInfo">ArrivalInfo</a>]</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>displayName</th>
        <td>취급 역명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td>운영사에서 취급하는 역사명</td>
    </tr>
    <tr>
        <th>stationId</th>
        <td>실시간 도착 정보 역ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

### /timetable

전철/지하철 시간표를 불러옵니다.

```
https://api.yhs.kr/metro/timetable
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
        <td>역사 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>direction</th>
        <td>방향</td>
        <td>integer</td>
        <td>X</td>
        <td>0</td>
        <td></td>
    </tr>
    <tr>
        <th>weekType</th>
        <td>시간표 유형</td>
        <td>integer</td>
        <td>X</td>
        <td>0</td>
        <td>
            0: 평일<br/>
            1: 주말(토요일)<br/>
            2: 일요일/공휴일<br/>
        </td>
    </tr>
</table>

#### Return

```json
[
  {
    "destination": "인천",
    "direction": 1,
    "hours": 5,
    "id": "1812",
    "minutes": 0,
    "name": "인천",
    "seconds": 0,
    "week_type": 2
  }
]
```

* 기본 객체

<table>
    <tr>
        <th>destination</th>
        <td>목적지</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>direction</th>
        <td>방향</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>hours</th>
        <td>시간</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>id</th>
        <td>역사 ID</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>minutes</th>
        <td>분</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>name</th>
        <td>역사 명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>seconds</th>
        <td>초</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>weekType</th>
        <td>시간표 유형</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td>
            0: 평일<br/>
            1: 주말(토요일)<br/>
            2: 일요일/공휴일<br/>
        </td>
    </tr>
</table>
