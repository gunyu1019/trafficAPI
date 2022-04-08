# 수도권 지하철 역사 / 도착정보 / 시간표 안내

아래에는 수도권 지역의 지하철/전철 역사 정보, 시간표 및 실시간 도착 정보에 대하여 서술되어 있습니다.

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