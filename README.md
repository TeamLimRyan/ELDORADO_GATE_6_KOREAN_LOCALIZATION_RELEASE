# 엘도라도 게이트 제6권 한국어 패치 1.0

드림캐스트 일본판 **엘도라도 게이트 제6권**의 비공식 한국어 패치입니다. 게임 대사·메뉴·도움말과 게임 내 이미지의 한국어화, 한글 폰트, 반각 공백을 적용했습니다.

원본 게임 파일은 포함하지 않습니다. 직접 준비한 동일 판본의 원본에 적용하세요.

## 다운로드

[최신 릴리스](https://github.com/TeamLimRyan/ELDORADO_GATE_6_KOREAN_LOCALIZATION_RELEASE/releases/latest)에서 **Eldorado_Gate_6_Korean_v1.0.zip**을 받으세요. 설치기와 패치가 함께 들어 있습니다.

별도 `.xdelta` 파일은 원본 GDI의 **3번 트랙**에 적용하는 차분입니다. CHD 파일에 직접 적용하지 마세요.

## 대상 원본

- 일본판 T1228M / V1.001
- 원본 CHD 크기: 447,703,423바이트
- 원본 CHD SHA-256: `4f7a3f76d4d91570aef0dc097179f77ebcefa78f2ec0757a534bf8839565b6b4`
- GDI 입력은 `manifest.json`의 세 트랙 크기·SHA-256과 모두 일치해야 합니다.

CHD의 압축 방식이 달라 해시가 다르면 GDI로 추출한 뒤 트랙 해시가 일치하는지 확인하세요. 다른 권이나 다른 판본에는 적용할 수 없습니다.

## 설치

Windows 10/11 x64, Python 3.11 이상, 출력용 여유 공간 5GiB 이상이 필요합니다. Python 추가 패키지는 필요하지 않습니다.

1. ZIP을 새 폴더에 풉니다.
2. 해당 폴더에서 터미널을 엽니다.
3. 원본과 별도의 **새 출력 폴더**를 지정해 실행합니다.

GDI 원본:

```text
python apply_patch.py --input "원본/disc.gdi" --output "한국어_제6권"
```

CHD 원본은 [MAME 공식 배포](https://www.mamedev.org/release.html)의 `chdman`이 추가로 필요합니다. `chdman.exe` 경로를 지정합니다.

```text
python apply_patch.py --input "Eldorado Gate Dai-6-kan (Japan).chd" --output "한국어_제6권" --chdman "도구/chdman.exe"
```

완료되면 출력 폴더의 `disc.gdi`를 에뮬레이터에서 여세요. 함께 생성된 트랙 파일도 같은 폴더에 두어야 합니다. 설치기는 원본과 패치 해시를 확인하고, 출력 파일이 배포 기준 SHA-256과 일치해야 성공으로 처리합니다.

원본과 기존 출력 폴더를 덮어쓰지 않습니다. 실패한 경우 `diagnostics.json`을 확인하고 새 출력 폴더로 다시 실행하세요. 제거하려면 생성한 출력 폴더를 삭제하면 됩니다. 저장 데이터는 에뮬레이터에서 별도로 백업하세요.

## 적용 내용과 제한

- 게임 본편 대사, 메뉴, 시스템 안내, 명칭 및 게임 내 이미지 한국어화
- 한글 폰트와 반각 공백 적용
- Dream Passport 로컬 화면 일부 한국어화. 영문 키보드의 일부 기능 표기는 일본어로 남아 있습니다.
- 음성·영상과 BIOS/VMU 시스템 화면은 원문을 유지합니다.
- Dream Passport의 원격 온라인 기능은 지원하지 않습니다.
- 검증 환경은 Windows x64의 Flycast libretro HLE입니다. 드림캐스트 실기 동작은 확인하지 않았습니다.
- 일본어판과의 저장 데이터 역호환은 보장하지 않습니다.

## 문제 제보

[Issues](https://github.com/TeamLimRyan/ELDORADO_GATE_6_KOREAN_LOCALIZATION_RELEASE/issues)에 패치 버전, 실행 환경, 재현 절차와 화면을 남겨 주세요. 설치 문제는 개인정보와 로컬 경로를 가린 `diagnostics.json`을 함께 제공하면 도움이 됩니다. 원본 게임 파일이나 BIOS는 올리지 마세요.

## 저작권 및 라이선스

원작의 권리는 CAPCOM 및 각 권리자에게 있습니다. 본 패치는 비공식 팬 번역이며 원작 권리자와 관계가 없습니다. 설치기는 MIT, 동봉 xdelta3는 GPL-2.0-or-later입니다. 글꼴은 Galmuri와 나눔고딕을 사용하며 각 SIL Open Font License를 동봉했습니다. 자세한 내용은 `LICENSES`를 참조하세요.
