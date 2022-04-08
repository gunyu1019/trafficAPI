# 서울시 공공자전거 (비공식)
아래에는 서울시 공공자전거 (따릉이) 대여소 안내에 대해 서술되어 있습니다.

### /query

자전거 대여소를 검색합니다.

```
https://api.yhs.kr/bike/query
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
        <td>대여소 명칭</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

#### Return

```json
{
  "data": [
    {
      "id": "ST-4",
      "name": "102. 망원역 1번출구 앞",
      "parking": 20,
      "posX": 126.91062927,
      "posY": 37.5556488,
      "rests": 24,
      "shared": 120
    }
  ],
  "lastUpdate": 0
}
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
        <th>lastUpdate</th>
        <td>마지막 업데이트</td>
        <td>float</td>
        <td>X</td>
        <td></td>
        <td>timestamp 제공</td>
    </tr>
    <tr>
        <th>data</th>
        <td>대여소 상황</td>
        <td>list[QueryBikeStation]</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

* QueryBikeStation 객체

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
        <td>대여소 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>name</th>
        <td>대여소 명</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>parking</th>
        <td>최대 반납 가능한 자릿수</td>
        <td>integer</td>
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
        <th>rests</th>
        <td>반납 가능한 자릿 수</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>shared</th>
        <td>공유현황</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

### /bike/around

좌표 값을 기준으로 주변에 있는 자전거 대여소 정보를 불러옵니다.

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
</table>

#### Return

```json
{
  "data": [
      {
          "direction": -51,
          "distance": 64.4,
          "id": "ST-4",
          "name": "102. 망원역 1번출구 앞",
          "parking": 20,
          "posX": 126.91062927,
          "posY": 37.5556488,
          "rests": 17,
          "shared": 85
      }
  ],
  "lastUpdate": 1649434003.6246
}
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
        <th>lastUpdate</th>
        <td>마지막 업데이트</td>
        <td>float</td>
        <td>X</td>
        <td></td>
        <td>timestamp 제공</td>
    </tr>
    <tr>
        <th>data</th>
        <td>대여소 상황</td>
        <td>list[AroundBikeStation]</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>

* AroundBikeStation 객체

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
        <td>대여소 ID</td>
        <td>string</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>direction</th>
        <td>대여소 방향</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>distance</th>
        <td>대여소까지 거리(m)</td>
        <td>float</td>
        <td>O</td>
        <td></td>
        <td></td>
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
        <th>parking</th>
        <td>최대 반납 가능한 자릿수</td>
        <td>integer</td>
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
        <th>rests</th>
        <td>반납 가능한 자릿 수</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>shared</th>
        <td>공유현황</td>
        <td>integer</td>
        <td>O</td>
        <td></td>
        <td></td>
    </tr>
</table>
