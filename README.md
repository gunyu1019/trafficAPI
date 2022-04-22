<h1 align="center">Traffic API</h1>
<p align="center">
  수도권 교통 정보를 보다 쉽게 조회할 수 있는 API 입니다.
</p>

# Introduce
수도권 대중교통 정보를 제공합니다.
* 버스 정류장 정보
* 버스 실시간 도착 정보
* 수도권 지하철 역사 정보
* 수도권 지하철 도착 정보
* 수도권 지하철 시간표 정보
* 서울특별시 실시간 대여자전거 정보

# Documentation
아래 링크를 클릭하여 본 API의 사용 방법을 알아보세요!
* [한국어 문서](docs/)
  * [수도권 버스 정류소/버스 도착 정보](docs/bus.md)
  * [수도권 전철 역사/전철 도착 정보](docs/metro.md)
  * [서울특별시 대여자전거 정보](docs/bike.md)

# Source
각 대중교통 정보의 출처는 다음과 같습니다.<br/>
일부 정보는 TrafficAPI에 알맞게 수정된 데이터도 일부 있습니다.

### 버스 정류장 정보 / 버스 실시간 도착 정보
* 수도권: 
  * [서울특별시](https://bus.go.kr/)
  * [경기도(GBIS)](http://www.gbis.go.kr/)
  * [인천광역시](http://bus.incheon.go.kr/)
* 부산·울산권(부울권): 
  * [부산광역시](http://bus.busan.go.kr/)
  * [울산광역시](http://its.ulsan.kr/)
  * [창원시](http://bus.changwon.go.kr/)
  * [김해시](http://bus.gimhae.go.kr/) - 국가대중교통정보센터(TAGO)
* ~~광주권:~~ - 지원 예정
  * [광주광역시](http://bus.gwangju.go.kr/)
  * [나주시](http://bus.gwangju.go.kr/)
  * [담양군](http://bis.damyang.go.kr/)
  * 장성군(일부) - 광주광역시
  * [화순군](http://bis.hwasun.go.kr/main/main)

### 지하철 역사 / 실시간 도착 / 시간표 정보
* 서울교통공사
* [henewsuh/subway_crd_line_info](https://github.com/henewsuh/subway_crd_line_info) - 시간표 정보, 2022년 전철 반영

### 자전거 대여소 정보
* [서울특별시 따릉이](https://www.bikeseoul.com/)