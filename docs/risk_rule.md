# Pet Adoption Retention-Risk Rules

## Rule 1: First-Time Owner + High-Energy Pet
**CONDITIONS:**
- Adopter: experience_level = 'first_time'
- Pet: age in ['Baby', 'Young'] AND size in ['Large', 'Extra Large']
  OR breed contains high-energy keywords (Husky, Border Collie, Jack Russell, etc.)

**RISK:** First-time owners often underestimate the time, energy, and training required for high-energy breeds. Can lead to behavioral issues and early returns.

**GUIDANCE:** 
- Enroll in puppy/dog training classes within first 2 weeks
- Commit to 60-90 minutes of daily exercise
- Research breed-specific needs and common challenges
- Join local dog owner groups for support

**WEIGHT:** 25 points

---

## Rule 2: Young Children + Large Adolescent Dog
**CONDITIONS:**
- Adopter: has_kids = True AND 'toddler' in kid_ages
- Pet: age in ['Young', 'Baby'] AND size in ['Large', 'Extra Large']

**RISK:** Young dogs are naturally mouthy and jump. Large breeds can easily knock over small children, leading to injuries and fear.

**GUIDANCE:**
- Work with certified trainer on gentle behavior from day one
- Supervise ALL interactions between child and pet
- Teach children proper pet handling
- Consider waiting until children are older or choosing smaller/calmer pet

**WEIGHT:** 40 points

---

## Rule 3: Limited Exercise Time + Working/Herding Breed
**CONDITIONS:**
- Adopter: daily_exercise_minutes < 30
- Pet: breed contains working/herding keywords (Border Collie, Australian Shepherd, Belgian Malinois, Cattle Dog, German Shepherd, etc.)

**RISK:** Working breeds require significant physical and mental stimulation. Without it, they develop destructive behaviors, anxiety, and can become difficult to manage.

**GUIDANCE:**
- Increase daily exercise commitment to minimum 60 minutes
- Add mental stimulation: puzzle toys, training sessions, nose work
- Consider doggy daycare 2-3 times per week
- Alternatively, choose a lower-energy breed better suited to lifestyle

**WEIGHT:** 35 points

---

## Rule 4: Apartment Living + Very Vocal Breed
**CONDITIONS:**
- Adopter: home_type = 'apartment' AND noise_tolerance = 'low'
- Pet: breed contains vocal keywords (Husky, Beagle, Hound, Chihuahua, Terrier, etc.)

**RISK:** Vocal breeds are prone to barking, howling, and "talking." In apartments with shared walls, this leads to neighbor complaints and potential eviction.

**GUIDANCE:**
- Budget for professional trainer specializing in quiet commands
- Start training immediately upon adoption
- Discuss with neighbors upfront about training period
- Consider soundproofing measures
- Choose quieter breed if noise is dealbreaker

**WEIGHT:** 20 points

---

## Rule 5: Allergies + Heavy Shedding Breed
**CONDITIONS:**
- Adopter: allergies in ['mild', 'moderate', 'severe']
- Pet: breed contains shedding keywords (Husky, German Shepherd, Golden Retriever, Lab, Corgi, etc.)
  OR description mentions shedding

**RISK:** Even mild allergies can worsen with constant exposure to dander and shed fur. Severe cases force returns and can affect household health.

**GUIDANCE:**
- Consult allergist before adoption
- Commit to weekly professional grooming
- Invest in HEPA air filters for home
- Keep pet out of bedrooms
- Consider hypoallergenic breeds (Poodle, Bichon, Portuguese Water Dog)

**WEIGHT:** 30 points

---

## Rule 6: No Yard + Large High-Energy Dog
**CONDITIONS:**
- Adopter: yard_size = 'none' AND home_type = 'apartment'
- Pet: size in ['Large', 'Extra Large'] AND age in ['Young', 'Baby']

**RISK:** Large dogs without outdoor space require multiple daily walks and dedicated exercise time. Easy to under-exercise, leading to behavior problems.

**GUIDANCE:**
- Commit to 3+ walks daily (morning, midday, evening)
- Find nearby dog parks or trails
- Budget for dog walker if working full-time
- Consider smaller or lower-energy pet

**WEIGHT:** 20 points

---

## Rule 7: Full-Time Office Work + Separation Anxiety Risk
**CONDITIONS:**
- Adopter: work_schedule = 'full_time_office' (gone 8+ hours)
- Pet: age = 'Baby' OR description mentions "shy", "anxious", "needs companion"

**RISK:** Young puppies and anxious pets can develop separation anxiety when left alone for long periods. Results in destructive behavior and stress.

**GUIDANCE:**
- Arrange for midday dog walker or pet sitter
- Consider doggy daycare 3-5 days per week
- Crate train properly from day one
- Start with shorter absences and gradually increase
- Choose more independent adult pet if schedule inflexible

**WEIGHT:** 25 points

---

## Rule 8: No Other Pets + "Must Be Only Pet"
**CONDITIONS:**
- Adopter: has_other_pets = True
- Pet: description contains "only pet", "no other animals", "cat aggressive", "dog aggressive"

**RISK:** Direct incompatibility. Pet's behavioral needs conflict with household situation.

**GUIDANCE:**
- This is a dealbreaker - do not proceed with this match
- Search for pets marked as good with other animals
- Work with shelter on slow introduction if considering anyway

**WEIGHT:** 50 points (highest - this is a hard incompatibility)

---

## Rule 9: Limited Training Commitment + Strong-Willed Breed
**CONDITIONS:**
- Adopter: training_commitment = 'limited'
- Pet: breed contains stubborn/independent keywords (Husky, Shiba Inu, Terriers, Hounds, Chow, etc.)

**RISK:** Independent breeds require consistent, patient training. Without commitment, they become unmanageable and develop bad habits.

**GUIDANCE:**
- Reconsider training commitment - these breeds require structure
- Hire professional trainer if unable to commit personal time
- Choose easier-to-train breed (Golden Retriever, Lab, Poodle)
- Read breed-specific training resources before deciding

**WEIGHT:** 20 points

---

## Rule 10: Senior Pet + First-Time Owner Without Preparation
**CONDITIONS:**
- Adopter: experience_level = 'first_time'
- Pet: age = 'Senior'

**RISK:** Senior pets may have special medical needs, behavioral quirks from past experiences, and shorter lifespan. First-time owners may be unprepared for costs and emotional aspects.

**GUIDANCE:**
- Research senior pet care and common health issues
- Budget for potential vet expenses (often higher for seniors)
- Understand end-of-life care may come sooner
- Consult with shelter about this specific senior's needs
- Senior pets can be wonderful for prepared adopters!

**WEIGHT:** 15 points (lower weight - more of awareness flag than risk)
