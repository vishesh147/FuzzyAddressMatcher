from text_matcher import TextAddress
from geo_matcher import GeoAddress

input_address = TextAddress(input("Enter address: ").strip())

scores = []
fuzz_score_data = []
soundex_score_data = []

soundex_weight = 0.2

with open('data/addresses.txt') as fp:
    for line in fp:
        addr = TextAddress(line.strip())
        fuzz_score = input_address.match_score(addr)
        fuzz_score_data.append(fuzz_score)
        soundex_score = input_address.soundex_score(addr)        
        soundex_score_data.append(soundex_score)
        composite_score = (1-soundex_weight)*fuzz_score + soundex_weight*soundex_score
        scores.append((addr, int(composite_score)))

sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

input_geo_addr = GeoAddress(input_address.original_address)

print("\nClosest Address: ", sorted_scores[0][0].original_address)
print("Text Match Score: ", sorted_scores[0][1])
print("Geo Match Score: ", input_geo_addr.geo_match_score(GeoAddress(sorted_scores[0][0].original_address)))

with open('results/test_report.txt', 'w+') as f:
    for addr, score in sorted_scores:
        f.write(f'{addr.original_address:140}: {score}\n')
