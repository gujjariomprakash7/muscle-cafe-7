"""Educational, equipment-flexible workout builder for Muscle Cafe.

Exercise labels describe a training emphasis, not complete isolation of one
muscle head. Individual anatomy and exercise tolerance vary between people.
"""

EQUIPMENT_OPTIONS = [
    "Barbell",
    "Dumbbells",
    "Cable",
    "Machine",
    "Smith Machine",
    "Resistance Band",
    "Kettlebell",
    "Suspension Trainer",
]

# The focus labels are deliberately anatomical but beginner-readable.
# The notes explain where true head-by-head isolation is not possible.
FOCUS_GUIDE = {
    "Chest": {
        "Upper chest (clavicular fibres)": {
            "summary": "The clavicular fibres are the upper portion of the pectoralis major. Incline presses and low-to-high fly paths can place more emphasis on this region.",
            "limitation": "This is a regional emphasis, not a separate muscle head that can be isolated. The whole pectoralis major contributes to pressing and fly movements.",
        },
        "Middle chest (sternocostal fibres)": {
            "summary": "The sternocostal portion forms much of the pectoralis major. Flat presses and chest-height fly movements train the chest through horizontal pressing or adduction.",
            "limitation": "The chest works as a coordinated muscle; exercise angles change emphasis rather than switching individual fibres completely on or off.",
        },
        "Lower chest (lower sternal fibres)": {
            "summary": "A slight decline pressing angle or a high-to-low cable path can emphasise the lower fibres of the pectoralis major.",
            "limitation": "There is no completely separate lower-chest muscle. Dips and decline work still involve the pectoralis major as a whole.",
        },
    },
    "Back": {
        "Lats (latissimus dorsi)": {
            "summary": "The latissimus dorsi helps bring the upper arm down and toward the body. Pull-ups, pulldowns and rows with the elbows closer to the torso train it.",
            "limitation": "Different grips and elbow paths can change emphasis, but they do not isolate a distinct upper or lower lat head.",
        },
        "Upper back (rhomboids and middle traps)": {
            "summary": "Rows with the elbows travelling somewhat away from the torso and controlled shoulder-blade retraction involve the rhomboids and middle trapezius.",
            "limitation": "The upper back is a group of muscles, not one muscle head. Rows also involve the lats, rear delts and arm muscles.",
        },
        "Lower traps": {
            "summary": "The lower trapezius helps control the shoulder blade, including upward rotation and posterior tilt. Prone Y raises and cable Y raises are useful options.",
            "limitation": "Lower-trap work is coordination-focused; use light, controlled loads rather than swinging or forcing range.",
        },
        "Spinal erectors (lower back)": {
            "summary": "The spinal erectors help extend and stabilise the spine. Hip hinges and controlled back extensions train them alongside other posterior-chain muscles.",
            "limitation": "These are not a bodybuilding 'lower-back head'. Use a comfortable range and avoid treating spinal pain with exercise advice from an app.",
        },
    },
    "Shoulders": {
        "Front deltoid (anterior head)": {
            "summary": "The anterior deltoid helps raise the arm forward. Overhead presses and front raises train it; chest presses also involve it.",
            "limitation": "The three deltoid heads work together to stabilise and move the shoulder. Pressing is not an anterior-delt-only movement.",
        },
        "Side deltoid (lateral head)": {
            "summary": "The lateral deltoid is strongly involved in raising the arm out to the side. Dumbbell, cable and machine lateral raises are direct options.",
            "limitation": "There is no need to force very heavy lateral raises. Use a smooth, comfortable range; overhead presses involve the side delts but usually also load the front delts and triceps substantially.",
        },
        "Rear deltoid (posterior head)": {
            "summary": "The posterior deltoid helps move the arm backward and out horizontally. Reverse fly variations and rear-delt rows are useful options.",
            "limitation": "Rows also train the upper back. Keep the movement controlled and avoid turning a rear-delt fly into a body swing.",
        },
    },
    "Biceps": {
        "Biceps brachii — long head": {
            "summary": "The long head is one of the two heads of the biceps brachii and crosses the shoulder joint. Incline curls and behind-the-body cable curls place the shoulder in extension and train the biceps at a longer muscle length.",
            "limitation": "No curl perfectly isolates the long head. Both biceps heads contribute to elbow flexion and forearm supination; treat this as an emphasis, not an isolation guarantee.",
        },
        "Biceps brachii — short head": {
            "summary": "The short head is the other head of the biceps brachii. Standard supinated curls and some curls with the upper arm slightly forward can train the biceps effectively.",
            "limitation": "Grip width and arm position do not switch the long head off. Both heads contribute to most conventional curl variations.",
        },
        "Brachialis (separate elbow-flexor muscle)": {
            "summary": "The brachialis sits underneath the biceps and is an important elbow flexor. Hammer curls and reverse curls reduce the biceps' mechanical advantage compared with a fully supinated curl.",
            "limitation": "The brachialis is not a head of the biceps. It works alongside the biceps and brachioradialis during elbow flexion.",
        },
    },
    "Triceps": {
        "Triceps — long head": {
            "summary": "The long head crosses both the shoulder and elbow. Overhead cable or dumbbell extensions place it at a longer length because the arm is raised overhead.",
            "limitation": "All three triceps heads contribute to elbow extension. Overhead work emphasises the long head's lengthened position but does not isolate it.",
        },
        "Triceps — lateral head": {
            "summary": "The lateral head contributes to elbow extension. Pushdowns and pressing movements train the triceps, including this head.",
            "limitation": "There is no reliable exercise that completely isolates the lateral head from the medial and long heads. Use this selection as general triceps work with a lateral-head label for learning anatomy, not as a guarantee of selective growth.",
        },
        "Triceps — medial head": {
            "summary": "The medial head contributes to elbow extension across many loads and joint positions. Controlled pushdowns and close-grip pressing involve it.",
            "limitation": "The medial head cannot be cleanly isolated from the other triceps heads with a particular grip. The app shows useful movements but does not claim selective activation.",
        },
    },
    "Quads": {
        "Rectus femoris": {
            "summary": "The rectus femoris crosses both the hip and knee. Knee extensions train the quadriceps directly; squat and split-squat patterns also load it while involving the other quadriceps muscles.",
            "limitation": "You cannot fully isolate rectus femoris from the vasti in normal gym exercises. The app labels a knee-extension emphasis, not exclusive activation.",
        },
        "Vastus lateralis": {
            "summary": "The vastus lateralis is the outer portion of the quadriceps group. Squats, leg presses, split squats and knee extensions all involve it.",
            "limitation": "Foot angle and stance tricks do not reliably isolate the vastus lateralis. All four quadriceps muscles contribute to knee extension.",
        },
        "Vastus medialis": {
            "summary": "The vastus medialis is the inner portion of the quadriceps group. It works during knee extension in squats, split squats, leg presses and leg extensions.",
            "limitation": "The 'VMO-only' idea is overstated: normal exercise cannot completely isolate the vastus medialis from the other quadriceps muscles.",
        },
        "Quadriceps overall (all four muscles)": {
            "summary": "The quadriceps includes rectus femoris, vastus lateralis, vastus medialis and vastus intermedius. Squat, leg-press, split-squat and knee-extension patterns train the group.",
            "limitation": "This is a muscle group with four muscles, not four independently selectable switches. Train it through a comfortable range with progressive resistance.",
        },
    },
    "Hamstrings": {
        "Biceps femoris — long head": {
            "summary": "The long head of biceps femoris crosses the hip and knee. Hip hinges such as Romanian deadlifts train it in a lengthened position; curls train its knee-flexion function.",
            "limitation": "Hamstring exercises involve several muscles. No movement isolates the long head completely.",
        },
        "Biceps femoris — short head": {
            "summary": "The short head of biceps femoris crosses the knee but not the hip, so knee-flexion exercises such as seated, lying and cable curls are relevant options.",
            "limitation": "Knee curls also involve the other hamstrings. Hip hinges alone do not train the short head as directly because it does not cross the hip.",
        },
        "Semitendinosus and semimembranosus": {
            "summary": "These medial hamstring muscles contribute to hip extension and knee flexion. Romanian deadlifts and leg-curl variations train them.",
            "limitation": "You cannot reliably isolate one medial hamstring from the others with a simple toe-angle change.",
        },
        "Hamstrings overall": {
            "summary": "The hamstrings work at both the hip and knee. Combining a hip hinge with a knee-curl pattern covers these two major functions.",
            "limitation": "A balanced hamstring plan uses more than one movement pattern rather than relying only on deadlifts or only on curls.",
        },
    },
    "Glutes": {
        "Gluteus maximus": {
            "summary": "The gluteus maximus is a major hip extensor. Hip thrusts, bridges, hinges, split squats and step-ups can train it.",
            "limitation": "The upper and lower portions are not separate heads that can be switched on independently. Exercise position changes emphasis and range.",
        },
        "Gluteus medius and minimus": {
            "summary": "The gluteus medius and minimus help move the thigh out to the side and stabilise the pelvis. Hip abduction and controlled single-leg work train them.",
            "limitation": "These are separate muscles, not upper and lower heads of gluteus maximus. Hip-abduction exercises also involve other stabilisers.",
        },
    },
    "Calves": {
        "Gastrocnemius (medial and lateral heads)": {
            "summary": "The gastrocnemius has medial and lateral heads and crosses the knee. Straight-knee calf raises train it while also involving the soleus.",
            "limitation": "The medial and lateral gastrocnemius heads cannot be cleanly isolated from one another by turning the feet in or out.",
        },
        "Soleus": {
            "summary": "The soleus lies beneath the gastrocnemius and does not cross the knee. Bent-knee calf raises, such as seated calf raises, place relatively more emphasis on it.",
            "limitation": "Seated calf raises still involve the calf complex; they do not turn the gastrocnemius completely off.",
        },
    },
    "Core": {
        "Rectus abdominis": {
            "summary": "The rectus abdominis helps flex the trunk and resist extension. Crunches, reverse crunches and controlled rollouts train it in different ways.",
            "limitation": "There are not separate upper and lower abdominal muscles. Different exercises may change emphasis, but the rectus abdominis is one continuous muscle.",
        },
        "Obliques": {
            "summary": "The internal and external obliques help rotate, side-bend and resist rotation of the trunk. Woodchops, side planks and Pallof presses train these functions.",
            "limitation": "The obliques work together with other trunk muscles. A single exercise does not isolate one oblique layer completely.",
        },
        "Deep core and trunk stability": {
            "summary": "The abdominal wall and other trunk muscles help resist unwanted movement. Planks, dead bugs and Pallof presses train bracing and stability.",
            "limitation": "'Deep core' is a broad coaching term, not one muscle. These exercises train coordinated trunk control.",
        },
    },
    "Traps": {
        "Upper trapezius": {
            "summary": "The upper trapezius helps elevate and rotate the shoulder blade. Shrugs and loaded carries train it.",
            "limitation": "The trapezius has upper, middle and lower regions that cooperate. Shrugs do not isolate every upper-trap fibre.",
        },
        "Middle trapezius": {
            "summary": "The middle trapezius helps retract the shoulder blades. Controlled rows and reverse-fly patterns involve it with the rhomboids and rear delts.",
            "limitation": "Rows train several upper-back muscles together; the middle traps are not isolated by simply squeezing the shoulder blades harder.",
        },
        "Lower trapezius": {
            "summary": "The lower trapezius helps control shoulder-blade upward rotation and posterior tilt. Prone or cable Y raises are useful light-load options.",
            "limitation": "Prioritise control and shoulder comfort. Heavy loads are usually unnecessary for learning this movement.",
        },
    },
    "Forearms": {
        "Brachioradialis": {
            "summary": "The brachioradialis is an elbow flexor on the forearm. Hammer curls and reverse curls train it while also involving other elbow flexors.",
            "limitation": "It is not a biceps head. These exercises also involve the brachialis and, depending on grip, the biceps.",
        },
        "Wrist flexors and grip": {
            "summary": "The wrist flexors help curl the wrist and support gripping. Wrist curls and loaded carries can train these functions.",
            "limitation": "Grip strength involves several forearm and hand muscles. Avoid excessive wrist-curl volume if the wrist or elbow becomes irritated.",
        },
        "Wrist extensors": {
            "summary": "The wrist extensors lift the back of the hand and help stabilise the wrist. Reverse wrist curls and controlled band extensions are options.",
            "limitation": "Use light, controlled loads. These small muscles do not require maximal loading to be trained.",
        },
    },
    "Adductors": {
        "Hip adductors (inner thigh)": {
            "summary": "The adductors bring the thigh toward the body's midline and help stabilise the hip. Adductor-machine work, cable adduction and Copenhagen progressions train them.",
            "limitation": "The adductor group contains multiple muscles and also contributes during compound lower-body movements. Progress Copenhagen variations gradually.",
        },
    },
}

MUSCLE_GROUPS = list(FOCUS_GUIDE.keys())


def _exercise(
    group,
    focus,
    name,
    equipment,
    kind,
    pattern,
    reps,
    why,
    cue,
    supports=(),
):
    """Create one catalogue entry; supports lists related focus labels."""
    return {
        "muscle": group,
        "focus": focus,
        "name": name,
        "equipment": equipment,
        "movement_type": kind,
        "pattern": pattern,
        "reps": reps,
        "why_it_fits": why,
        "coaching_cue": cue,
        "supports": tuple(supports),
    }


# Reusable focus labels keep exercise-to-focus matching consistent.
CHEST_UP = "Upper chest (clavicular fibres)"
CHEST_MID = "Middle chest (sternocostal fibres)"
CHEST_LOW = "Lower chest (lower sternal fibres)"
BACK_LATS = "Lats (latissimus dorsi)"
BACK_UPPER = "Upper back (rhomboids and middle traps)"
BACK_LOWER_TRAPS = "Lower traps"
BACK_ERECTORS = "Spinal erectors (lower back)"
SH_FRONT = "Front deltoid (anterior head)"
SH_SIDE = "Side deltoid (lateral head)"
SH_REAR = "Rear deltoid (posterior head)"
BI_LONG = "Biceps brachii — long head"
BI_SHORT = "Biceps brachii — short head"
BI_BRACH = "Brachialis (separate elbow-flexor muscle)"
TRI_LONG = "Triceps — long head"
TRI_LAT = "Triceps — lateral head"
TRI_MED = "Triceps — medial head"
QUAD_RF = "Rectus femoris"
QUAD_VL = "Vastus lateralis"
QUAD_VM = "Vastus medialis"
QUAD_ALL = "Quadriceps overall (all four muscles)"
HAM_LONG = "Biceps femoris — long head"
HAM_SHORT = "Biceps femoris — short head"
HAM_MEDIAL = "Semitendinosus and semimembranosus"
HAM_ALL = "Hamstrings overall"
GLUTE_MAX = "Gluteus maximus"
GLUTE_MED = "Gluteus medius and minimus"
CALF_GASTRO = "Gastrocnemius (medial and lateral heads)"
CALF_SOLEUS = "Soleus"
CORE_ABS = "Rectus abdominis"
CORE_OBLIQUES = "Obliques"
CORE_STABILITY = "Deep core and trunk stability"
TRAP_UPPER = "Upper trapezius"
TRAP_MIDDLE = "Middle trapezius"
TRAP_LOWER = "Lower trapezius"
FOREARM_BRACHIO = "Brachioradialis"
FOREARM_FLEXORS = "Wrist flexors and grip"
FOREARM_EXTENSORS = "Wrist extensors"
ADDUCTOR_FOCUS = "Hip adductors (inner thigh)"

ALL_BICEPS = (BI_LONG, BI_SHORT, BI_BRACH)
ALL_TRICEPS = (TRI_LONG, TRI_LAT, TRI_MED)
ALL_QUADS = (QUAD_RF, QUAD_VL, QUAD_VM, QUAD_ALL)
ALL_HAMSTRINGS = (HAM_LONG, HAM_SHORT, HAM_MEDIAL, HAM_ALL)

EXERCISES = [
    # CHEST: upper / middle / lower regional emphasis.
    _exercise("Chest", CHEST_UP, "Incline Barbell Press", "Barbell", "Compound", "incline_press", "6-10", "An incline press places more emphasis on the clavicular fibres while training the whole chest, shoulders and triceps.", "Keep shoulder blades supported and use an incline that feels comfortable."),
    _exercise("Chest", CHEST_UP, "Incline Dumbbell Press", "Dumbbells", "Compound", "incline_press", "8-12", "A dumbbell incline press allows each arm to move independently and emphasises the upper chest region.", "Lower with control; do not force a deep stretch."),
    _exercise("Chest", CHEST_UP, "Incline Chest Press", "Machine", "Compound", "incline_press", "8-12", "A machine incline press is a stable alternative to free-weight pressing.", "Adjust the seat so the handles begin around upper-chest level."),
    _exercise("Chest", CHEST_UP, "Low-to-High Cable Fly", "Cable", "Isolation", "upper_fly", "10-15", "The upward arm path can emphasise the clavicular fibres during chest adduction.", "Use a light load and keep a soft bend in the elbows."),
    _exercise("Chest", CHEST_UP, "Incline Dumbbell Fly", "Dumbbells", "Isolation", "upper_fly", "10-15", "An incline fly trains the chest through horizontal adduction with an upper-chest emphasis.", "Use a modest range and avoid dropping the elbows too far below the torso."),
    _exercise("Chest", CHEST_MID, "Barbell Bench Press", "Barbell", "Compound", "flat_press", "6-10", "A horizontal press is a foundational compound chest movement.", "Keep wrists stacked over elbows and use a controlled touch point."),
    _exercise("Chest", CHEST_MID, "Flat Dumbbell Press", "Dumbbells", "Compound", "flat_press", "8-12", "A flat dumbbell press trains the pectoralis major with independent arm movement.", "Keep the weights controlled and avoid bouncing at the bottom."),
    _exercise("Chest", CHEST_MID, "Seated Chest Press", "Machine", "Compound", "flat_press", "8-12", "The machine press is a stable horizontal pressing option.", "Set the handles around mid-chest height."),
    _exercise("Chest", CHEST_MID, "Push-up", "Bodyweight", "Compound", "flat_press", "6-15", "A push-up is a bodyweight horizontal press for the chest, triceps and front delts.", "Keep the body in one line and scale with an incline if needed."),
    _exercise("Chest", CHEST_MID, "Cable Chest Fly", "Cable", "Isolation", "mid_fly", "10-15", "A chest-height fly trains horizontal adduction through a controlled range.", "Keep shoulders down and avoid letting the hands travel far behind the body."),
    _exercise("Chest", CHEST_MID, "Pec Deck Fly", "Machine", "Isolation", "mid_fly", "10-15", "The pec deck provides a stable chest-fly variation.", "Adjust the seat so elbows or handles align comfortably with the chest."),
    _exercise("Chest", CHEST_MID, "Dumbbell Fly", "Dumbbells", "Isolation", "mid_fly", "10-15", "A flat dumbbell fly loads the chest through horizontal adduction.", "Use lighter weights than a press and keep the elbows softly bent."),
    _exercise("Chest", CHEST_LOW, "Decline Barbell Press", "Barbell", "Compound", "decline_press", "6-10", "A decline press can place relatively more emphasis on lower sternal chest fibres.", "Use a secure bench setup and a spotter when needed."),
    _exercise("Chest", CHEST_LOW, "Decline Dumbbell Press", "Dumbbells", "Compound", "decline_press", "8-12", "A decline dumbbell press is a free-weight alternative for lower-chest emphasis.", "Start with a manageable load and secure your position before lifting."),
    _exercise("Chest", CHEST_LOW, "Chest Dip", "Bodyweight", "Compound", "chest_dip", "6-12", "A forward-leaning dip can train the chest and triceps with lower-chest emphasis.", "Only use a comfortable shoulder range; choose assisted dips if needed."),
    _exercise("Chest", CHEST_LOW, "High-to-Low Cable Fly", "Cable", "Isolation", "lower_fly", "10-15", "The downward arm path can emphasise lower sternal chest fibres.", "Move the arms down and in without rounding the shoulders."),
    _exercise("Chest", CHEST_LOW, "Decline Chest Press", "Machine", "Compound", "decline_press", "8-12", "A decline machine press provides a supported lower-chest pressing option.", "Set the handles so the movement feels smooth at the shoulder."),

    # BACK: lats, upper back, lower traps and spinal erectors.
    _exercise("Back", BACK_LATS, "Pull-up", "Bodyweight", "Compound", "vertical_pull", "5-10", "A vertical pull trains the lats along with elbow flexors and other upper-back muscles.", "Use assistance if needed; avoid swinging to complete reps."),
    _exercise("Back", BACK_LATS, "Lat Pulldown", "Machine", "Compound", "vertical_pull", "8-12", "A pulldown is a scalable vertical pull with strong lat involvement.", "Pull toward the upper chest without leaning far backward."),
    _exercise("Back", BACK_LATS, "Kneeling Cable Lat Pulldown", "Cable", "Compound", "vertical_pull", "8-12", "A cable pulldown lets you adjust the arm path to train shoulder adduction and extension.", "Keep ribs controlled and drive elbows toward the sides."),
    _exercise("Back", BACK_LATS, "Band Straight-Arm Pulldown", "Resistance Band", "Isolation", "straight_arm_pulldown", "12-20", "A straight-arm pulldown trains shoulder extension with less elbow-flexor contribution.", "Keep elbows softly bent and avoid turning it into a crunch."),
    _exercise("Back", BACK_LATS, "Dumbbell Pullover", "Dumbbells", "Isolation", "pullover", "10-15", "A pullover trains shoulder extension and can involve the lats and chest.", "Use a comfortable shoulder range and avoid excessive lower-back arching."),
    _exercise("Back", BACK_UPPER, "Barbell Bent-Over Row", "Barbell", "Compound", "horizontal_row", "6-10", "A horizontal row trains the upper back, lats, rear delts and elbow flexors.", "Brace the trunk and keep the spine position controlled."),
    _exercise("Back", BACK_UPPER, "Chest-Supported Dumbbell Row", "Dumbbells", "Compound", "horizontal_row", "8-12", "Chest support reduces the need to hold a bent-over torso while rowing.", "Pull elbows back smoothly without shrugging."),
    _exercise("Back", BACK_UPPER, "Seated Cable Row", "Cable", "Compound", "horizontal_row", "8-12", "A cable row trains the upper back and lats through shoulder extension and scapular movement.", "Avoid leaning back to move the weight."),
    _exercise("Back", BACK_UPPER, "Chest-Supported Row Machine", "Machine", "Compound", "horizontal_row", "8-12", "A supported row is a stable option for upper-back training.", "Adjust the seat so the handles start in a comfortable reach."),
    _exercise("Back", BACK_UPPER, "Inverted Row", "Bodyweight", "Compound", "horizontal_row", "6-12", "An inverted row is a bodyweight horizontal pull for the upper back and arms.", "Keep the body aligned and change bar height to scale difficulty."),
    _exercise("Back", BACK_UPPER, "Cable Face Pull", "Cable", "Isolation", "face_pull", "12-15", "Face pulls involve rear delts, upper-back muscles and external rotators.", "Pull toward eye level with control; do not overextend the lower back."),
    _exercise("Back", BACK_LOWER_TRAPS, "Incline Bench Y Raise", "Dumbbells", "Isolation", "y_raise", "10-15", "A light Y raise challenges lower-trap contribution to shoulder-blade control.", "Use very light weights and keep the thumbs angled upward."),
    _exercise("Back", BACK_LOWER_TRAPS, "Cable Y Raise", "Cable", "Isolation", "y_raise", "10-15", "The cable provides resistance through a Y-raise path for lower-trap coordination.", "Keep the movement smooth and stop if the shoulder feels pinchy."),
    _exercise("Back", BACK_ERECTORS, "Romanian Deadlift", "Barbell", "Compound", "hip_hinge", "6-10", "A hip hinge trains the posterior chain, including spinal erectors, glutes and hamstrings.", "Brace before each rep and hinge at the hips with a controlled spine position."),
    _exercise("Back", BACK_ERECTORS, "Back Extension", "Machine", "Compound", "back_extension", "10-15", "A controlled back extension trains the spinal erectors and hip extensors.", "Move through a comfortable range; do not hyperextend at the top."),
    _exercise("Back", BACK_ERECTORS, "Bird Dog", "Bodyweight", "Stability", "bird_dog", "8-12 each side", "Bird dog trains trunk and spinal stability with low external load.", "Keep hips level and reach slowly without rotating."),

    # SHOULDERS: anterior, lateral and posterior deltoid heads.
    _exercise("Shoulders", SH_FRONT, "Standing Barbell Overhead Press", "Barbell", "Compound", "overhead_press", "6-10", "A vertical press trains the anterior deltoid, triceps and other shoulder muscles.", "Use a comfortable path and avoid excessive rib flare."),
    _exercise("Shoulders", SH_FRONT, "Seated Dumbbell Shoulder Press", "Dumbbells", "Compound", "overhead_press", "8-12", "A dumbbell overhead press is a compound shoulder movement with strong front-delt involvement.", "Keep forearms reasonably vertical and lower only as far as comfortable."),
    _exercise("Shoulders", SH_FRONT, "Shoulder Press Machine", "Machine", "Compound", "overhead_press", "8-12", "A machine press offers a supported vertical-press alternative.", "Adjust the seat so the handles begin around shoulder height."),
    _exercise("Shoulders", SH_FRONT, "Cable Front Raise", "Cable", "Isolation", "front_raise", "10-15", "A front raise trains shoulder flexion with anterior-delt emphasis.", "Raise only to a comfortable height without swinging."),
    _exercise("Shoulders", SH_FRONT, "Dumbbell Front Raise", "Dumbbells", "Isolation", "front_raise", "10-15", "A dumbbell front raise is a simple anterior-delt isolation-style movement.", "Use light weights and keep the torso still."),
    _exercise("Shoulders", SH_SIDE, "Dumbbell Lateral Raise", "Dumbbells", "Isolation", "lateral_raise", "10-15", "A lateral raise directly trains shoulder abduction with lateral-delt emphasis.", "Lead with the elbows and stop at a comfortable height."),
    _exercise("Shoulders", SH_SIDE, "Single-Arm Cable Lateral Raise", "Cable", "Isolation", "lateral_raise", "10-15", "The cable maintains resistance through more of the lateral-raise path.", "Stand stable and avoid leaning to swing the handle."),
    _exercise("Shoulders", SH_SIDE, "Lateral Raise Machine", "Machine", "Isolation", "lateral_raise", "10-15", "The machine provides a guided lateral-raise option.", "Align the upper arms with the machine pads and move smoothly."),
    _exercise("Shoulders", SH_SIDE, "Band Lateral Raise", "Resistance Band", "Isolation", "lateral_raise", "12-20", "A band is a convenient lateral-delt option when weights or cables are busy.", "Keep tension controlled and avoid shrugging excessively."),
    _exercise("Shoulders", SH_SIDE, "Wide-Grip Cable Upright Row", "Cable", "Compound", "upright_row", "10-12", "A comfortable wide-grip upright row can involve lateral delts and upper traps as a multi-joint option.", "Use a pain-free range and stop below any uncomfortable shoulder height."),
    _exercise("Shoulders", SH_REAR, "Chest-Supported Rear-Delt Row", "Dumbbells", "Compound", "rear_delt_row", "8-12", "A rear-delt row uses a wider elbow path to involve posterior delts and upper-back muscles.", "Keep the chest supported and avoid turning the movement into a shrug."),
    _exercise("Shoulders", SH_REAR, "Reverse Pec Deck", "Machine", "Isolation", "rear_delt_fly", "10-15", "A reverse fly trains horizontal shoulder abduction with rear-delt emphasis.", "Keep the shoulders away from the ears and move without momentum."),
    _exercise("Shoulders", SH_REAR, "Bent-Over Dumbbell Reverse Fly", "Dumbbells", "Isolation", "rear_delt_fly", "10-15", "A dumbbell reverse fly trains the posterior deltoid and upper back.", "Use light weights and keep the torso stable."),
    _exercise("Shoulders", SH_REAR, "Cable Rear-Delt Fly", "Cable", "Isolation", "rear_delt_fly", "10-15", "The cable provides a rear-delt fly variation with adjustable resistance.", "Move the upper arms apart without twisting the trunk."),
    _exercise("Shoulders", SH_REAR, "Band Pull-Apart", "Resistance Band", "Isolation", "rear_delt_fly", "12-20", "A band pull-apart trains rear delts and scapular retractors with light resistance.", "Keep shoulders relaxed and control the return."),

    # BICEPS: long head, short head and the separate brachialis.
    _exercise("Biceps", "Overall biceps brachii", "Chin-up", "Bodyweight", "Compound", "vertical_pull", "5-10", "A chin-up is a compound vertical pull that trains both biceps heads along with the back.", "Use assistance or a band if needed; avoid kipping.", ALL_BICEPS),
    _exercise("Biceps", "Overall biceps brachii", "Underhand Lat Pulldown", "Machine", "Compound", "vertical_pull", "8-12", "An underhand pulldown combines a back movement with elbow flexion, involving both biceps heads.", "Keep the torso steady and bring elbows down smoothly.", ALL_BICEPS),
    _exercise("Biceps", BI_LONG, "Incline Dumbbell Curl", "Dumbbells", "Isolation", "incline_curl", "8-12", "The arm sits slightly behind the torso, placing the biceps at a longer shoulder position.", "Let the upper arm stay back and avoid swinging."),
    _exercise("Biceps", BI_LONG, "Behind-the-Body Cable Curl", "Cable", "Isolation", "long_length_curl", "10-15", "A behind-the-body cable curl trains elbow flexion with the shoulder extended.", "Keep the elbow slightly behind the torso and curl without rotating."),
    _exercise("Biceps", BI_LONG, "Bayesian Cable Curl", "Cable", "Isolation", "long_length_curl", "10-15", "This cable setup keeps the upper arm behind the body to train the biceps at a longer length.", "Use a controlled range and choose a load that does not pull the shoulder forward."),
    _exercise("Biceps", BI_SHORT, "Wide-Grip EZ-Bar Curl", "Barbell", "Isolation", "wide_supinated_curl", "8-12", "A supinated curl with the upper arm slightly forward can be used for a short-head emphasis.", "Do not use an excessively wide grip; both biceps heads still work."),
    _exercise("Biceps", BI_SHORT, "Preacher Curl Machine", "Machine", "Isolation", "preacher_curl", "10-15", "The preacher position places the upper arm in front of the torso and trains elbow flexion under control.", "Avoid bouncing or locking the elbow at the bottom."),
    _exercise("Biceps", BI_SHORT, "Dumbbell Preacher Curl", "Dumbbells", "Isolation", "preacher_curl", "10-15", "A dumbbell preacher curl is a single-arm alternative for controlled biceps work.", "Keep the upper arm supported and use a comfortable range."),
    _exercise("Biceps", "Overall biceps brachii", "Alternating Dumbbell Curl", "Dumbbells", "Isolation", "supinated_curl", "8-12", "A standard supinated curl trains both heads of the biceps brachii.", "Rotate only as comfortable and keep elbows near the sides.", ALL_BICEPS),
    _exercise("Biceps", "Overall biceps brachii", "EZ-Bar Curl", "Barbell", "Isolation", "supinated_curl", "8-12", "An EZ-bar curl trains both biceps heads with a comfortable semi-supinated grip.", "Keep wrists neutral and avoid using hip momentum.", ALL_BICEPS),
    _exercise("Biceps", BI_BRACH, "Dumbbell Hammer Curl", "Dumbbells", "Isolation", "hammer_curl", "8-12", "A neutral-grip curl involves the brachialis and brachioradialis strongly.", "Keep palms facing each other and elbows steady."),
    _exercise("Biceps", BI_BRACH, "Rope Hammer Curl", "Cable", "Isolation", "hammer_curl", "10-15", "A rope hammer curl is a cable alternative for neutral-grip elbow flexion.", "Separate the rope slightly at the top without swinging."),
    _exercise("Biceps", BI_BRACH, "Reverse EZ-Bar Curl", "Barbell", "Isolation", "reverse_curl", "10-15", "A pronated grip makes the brachialis and brachioradialis important elbow flexors.", "Use a lighter load and keep wrists straight."),

    # TRICEPS: all three heads work together; overhead position lengthens long head.
    _exercise("Triceps", "Overall triceps", "Close-Grip Bench Press", "Barbell", "Compound", "close_grip_press", "6-10", "A close-grip press is a compound push that trains all triceps heads with chest and front-delt assistance.", "Use a grip that keeps wrists comfortable; do not force an extremely narrow grip.", ALL_TRICEPS),
    _exercise("Triceps", "Overall triceps", "Parallel-Bar Dip", "Bodyweight", "Compound", "triceps_dip", "6-12", "A more upright dip can train the triceps as a compound elbow-extension movement.", "Use assistance if needed and stay within a comfortable shoulder range.", ALL_TRICEPS),
    _exercise("Triceps", "Overall triceps", "Assisted Dip Machine", "Machine", "Compound", "triceps_dip", "8-12", "The assisted dip machine offers a scalable compound triceps option.", "Set assistance so every repetition remains controlled.", ALL_TRICEPS),
    _exercise("Triceps", TRI_LONG, "Overhead Cable Triceps Extension", "Cable", "Isolation", "overhead_extension", "10-15", "The overhead arm position lengthens the biarticular long head of the triceps.", "Keep upper arms stable and avoid arching the lower back."),
    _exercise("Triceps", TRI_LONG, "Seated Dumbbell Overhead Extension", "Dumbbells", "Isolation", "overhead_extension", "10-15", "An overhead extension trains elbow extension with the long head at a longer shoulder position.", "Use a manageable dumbbell and keep elbows in a comfortable position."),
    _exercise("Triceps", TRI_LONG, "Overhead Rope Extension", "Cable", "Isolation", "overhead_extension", "10-15", "A rope is another way to load the triceps in an overhead position.", "Move at the elbows and keep ribs stacked over the pelvis."),
    _exercise("Triceps", TRI_LAT, "Cable Triceps Pushdown", "Cable", "Isolation", "pushdown", "10-15", "A pushdown trains elbow extension with all three triceps heads contributing, including the lateral head.", "Keep elbows near the sides and avoid rocking the torso."),
    _exercise("Triceps", TRI_LAT, "Straight-Bar Pushdown", "Cable", "Isolation", "pushdown", "10-15", "A straight-bar pushdown is a simple elbow-extension variation for the triceps.", "Use a comfortable wrist position and control the return.", ALL_TRICEPS),
    _exercise("Triceps", TRI_MED, "Reverse-Grip Cable Pushdown", "Cable", "Isolation", "reverse_pushdown", "10-15", "A reverse-grip pushdown is another controlled triceps extension; the medial head remains active with the other heads.", "Use a light load and keep the wrist aligned.", ALL_TRICEPS),
    _exercise("Triceps", TRI_MED, "Dumbbell Kickback", "Dumbbells", "Isolation", "kickback", "10-15", "A kickback trains elbow extension with the upper arm held behind the torso.", "Keep the upper arm still and avoid swinging the dumbbell.", ALL_TRICEPS),

    # QUADS: movements train the group; no toe-angle or machine trick isolates one vastus.
    _exercise("Quads", QUAD_ALL, "Barbell Back Squat", "Barbell", "Compound", "squat", "6-10", "A squat is a multi-joint knee- and hip-extension exercise involving all quadriceps muscles.", "Use a depth and stance that allow balance and comfortable control.", ALL_QUADS),
    _exercise("Quads", QUAD_ALL, "Goblet Squat", "Dumbbells", "Compound", "squat", "8-12", "The goblet squat is a beginner-friendly loaded squat for the quadriceps and glutes.", "Keep the weight close and knees tracking comfortably with the toes.", ALL_QUADS),
    _exercise("Quads", QUAD_ALL, "Smith Machine Squat", "Smith Machine", "Compound", "squat", "8-12", "A Smith squat is a guided squat variation that trains the quadriceps and glutes.", "Position feet so the movement feels natural; do not force a fixed stance.", ALL_QUADS),
    _exercise("Quads", QUAD_ALL, "Leg Press", "Machine", "Compound", "leg_press", "8-12", "A leg press trains knee extension with substantial quadriceps involvement.", "Keep hips supported and avoid lowering so far that the pelvis rolls under." , ALL_QUADS),
    _exercise("Quads", QUAD_ALL, "Bulgarian Split Squat", "Dumbbells", "Compound", "split_squat", "8-12 each leg", "A split squat trains each leg individually and loads the quadriceps and glutes.", "Use support for balance and keep the front foot fully planted.", ALL_QUADS),
    _exercise("Quads", QUAD_ALL, "Bodyweight Split Squat", "Bodyweight", "Compound", "split_squat", "10-15 each leg", "A bodyweight split squat is an accessible single-leg knee-extension pattern.", "Hold a stable support if balance is limiting.", ALL_QUADS),
    _exercise("Quads", QUAD_ALL, "Leg Extension", "Machine", "Isolation", "leg_extension", "10-15", "The leg extension trains knee extension and loads the quadriceps without a hip-hinge component.", "Align the knee with the machine pivot and use a pain-free range.", ALL_QUADS),
    _exercise("Quads", QUAD_ALL, "Band Leg Extension", "Resistance Band", "Isolation", "leg_extension", "12-20", "A band can provide a knee-extension alternative when a machine is occupied.", "Anchor the band securely and control both directions.", ALL_QUADS),

    # HAMSTRINGS: hip hinge and knee flexion train different functions.
    _exercise("Hamstrings", HAM_LONG, "Barbell Romanian Deadlift", "Barbell", "Compound", "hip_hinge", "6-10", "A hip hinge trains the long head of biceps femoris and medial hamstrings at the hip.", "Push hips back, keep the load close and stop at your controlled range.", (HAM_MEDIAL, HAM_ALL)),
    _exercise("Hamstrings", HAM_LONG, "Dumbbell Romanian Deadlift", "Dumbbells", "Compound", "hip_hinge", "8-12", "Dumbbells provide a flexible hip-hinge option for the hamstrings and glutes.", "Keep the weights close to the legs and avoid rounding to reach lower.", (HAM_MEDIAL, HAM_ALL)),
    _exercise("Hamstrings", HAM_LONG, "Smith Machine Romanian Deadlift", "Smith Machine", "Compound", "hip_hinge", "8-12", "A guided Romanian deadlift is another hip-hinge option for the biarticular hamstrings.", "Set the bar path and stance so hips can move back naturally.", (HAM_MEDIAL, HAM_ALL)),
    _exercise("Hamstrings", HAM_SHORT, "Seated Leg Curl", "Machine", "Isolation", "leg_curl_seated", "10-15", "Seated knee curls train the hamstrings as knee flexors with the hip flexed; the short head of biceps femoris is included.", "Keep hips against the pad and avoid using momentum.", (HAM_LONG, HAM_MEDIAL, HAM_ALL)),
    _exercise("Hamstrings", HAM_SHORT, "Lying Leg Curl", "Machine", "Isolation", "leg_curl_lying", "10-15", "A lying curl trains knee flexion and involves the short head of biceps femoris and other hamstrings.", "Keep hips down and control the lowering phase.", (HAM_LONG, HAM_MEDIAL, HAM_ALL)),
    _exercise("Hamstrings", HAM_SHORT, "Cable Leg Curl", "Cable", "Isolation", "leg_curl_cable", "10-15", "A cable ankle-strap curl is a flexible knee-flexion option for the hamstrings.", "Hold a stable support and avoid rotating the hip.", (HAM_LONG, HAM_MEDIAL, HAM_ALL)),
    _exercise("Hamstrings", HAM_SHORT, "Band Leg Curl", "Resistance Band", "Isolation", "leg_curl_band", "12-20", "A resistance band offers a knee-curl alternative when machines are unavailable.", "Anchor the band safely and keep the thigh still.", (HAM_LONG, HAM_MEDIAL, HAM_ALL)),
    _exercise("Hamstrings", HAM_ALL, "Nordic Hamstring Curl", "Bodyweight", "Compound", "nordic_curl", "4-8", "A Nordic curl heavily challenges the hamstrings during knee flexion and requires gradual progression.", "Use assistance and a pad; do not force repetitions beyond control.", (HAM_LONG, HAM_SHORT, HAM_MEDIAL)),
    _exercise("Hamstrings", HAM_ALL, "Glute-Ham Raise", "Machine", "Compound", "glute_ham_raise", "6-10", "The glute-ham raise combines hip and knee actions for the posterior thigh.", "Start with assistance and maintain trunk control.", (HAM_LONG, HAM_SHORT, HAM_MEDIAL)),

    # GLUTES: glute max hip extension and med/min hip abduction/stability.
    _exercise("Glutes", GLUTE_MAX, "Barbell Hip Thrust", "Barbell", "Compound", "hip_thrust", "8-12", "Hip thrusts train hip extension with strong gluteus maximus involvement.", "Finish with hips extended without over-arching the lower back."),
    _exercise("Glutes", GLUTE_MAX, "Dumbbell Glute Bridge", "Dumbbells", "Compound", "hip_thrust", "10-15", "A loaded bridge is a convenient hip-extension alternative.", "Keep ribs down and pause briefly at the top."),
    _exercise("Glutes", GLUTE_MAX, "Hip Thrust Machine", "Machine", "Compound", "hip_thrust", "8-12", "The machine provides a supported hip-thrust option for gluteus maximus.", "Set the pad securely and use a comfortable range."),
    _exercise("Glutes", GLUTE_MAX, "Smith Machine Hip Thrust", "Smith Machine", "Compound", "hip_thrust", "8-12", "A Smith-machine hip thrust is another way to load hip extension.", "Use padding and confirm the bar is secured before starting."),
    _exercise("Glutes", GLUTE_MAX, "Bulgarian Split Squat", "Dumbbells", "Compound", "glute_split_squat", "8-12 each leg", "A split squat with a comfortable longer stance can increase hip-extension demand on the front leg.", "Keep balance support nearby and avoid forcing stride length."),
    _exercise("Glutes", GLUTE_MAX, "Cable Glute Kickback", "Cable", "Isolation", "glute_kickback", "10-15", "A cable kickback trains hip extension with gluteus maximus emphasis.", "Keep pelvis still; do not arch the back to move the leg higher."),
    _exercise("Glutes", GLUTE_MAX, "Bodyweight Glute Bridge", "Bodyweight", "Compound", "hip_thrust", "12-20", "A bodyweight bridge is an accessible hip-extension exercise.", "Push through the whole foot and keep ribs stacked."),
    _exercise("Glutes", GLUTE_MAX, "Dumbbell Step-Up", "Dumbbells", "Compound", "step_up", "8-12 each leg", "Step-ups train hip and knee extension with glute involvement.", "Choose a step height that lets you control the ascent and descent."),
    _exercise("Glutes", GLUTE_MED, "Hip Abduction Machine", "Machine", "Isolation", "hip_abduction", "12-20", "Hip abduction trains gluteus medius and minimus as well as other lateral hip muscles.", "Move smoothly without bouncing the stack."),
    _exercise("Glutes", GLUTE_MED, "Standing Cable Hip Abduction", "Cable", "Isolation", "hip_abduction", "12-20", "A cable provides resistance while the leg moves out to the side.", "Keep the pelvis level and avoid leaning the trunk."),
    _exercise("Glutes", GLUTE_MED, "Side-Lying Hip Abduction", "Bodyweight", "Isolation", "hip_abduction", "12-20", "Side-lying abduction trains the lateral hip without gym equipment.", "Keep toes mostly forward and avoid rolling the pelvis backward."),
    _exercise("Glutes", GLUTE_MED, "Band Lateral Walk", "Resistance Band", "Isolation", "band_lateral_walk", "10-15 steps each way", "Lateral band walks challenge hip abductors and pelvic control.", "Use small controlled steps and keep band tension consistent."),

    # CALVES: straight-knee gastrocnemius bias and bent-knee soleus bias.
    _exercise("Calves", CALF_GASTRO, "Standing Calf Raise Machine", "Machine", "Isolation", "straight_knee_calf", "10-15", "A straight-knee calf raise emphasises the gastrocnemius while still involving soleus.", "Use a controlled stretch and pause at the top without bouncing."),
    _exercise("Calves", CALF_GASTRO, "Dumbbell Standing Calf Raise", "Dumbbells", "Isolation", "straight_knee_calf", "10-15", "A standing dumbbell calf raise is a free-weight option for the gastrocnemius and soleus.", "Hold a stable support and use a comfortable ankle range."),
    _exercise("Calves", CALF_GASTRO, "Single-Leg Calf Raise", "Bodyweight", "Isolation", "straight_knee_calf", "12-20", "A single-leg calf raise lets each side work independently.", "Use a wall or rail for balance and avoid bouncing."),
    _exercise("Calves", CALF_GASTRO, "Smith Machine Calf Raise", "Smith Machine", "Isolation", "straight_knee_calf", "10-15", "A Smith-machine calf raise is a loaded straight-knee alternative.", "Use a stable foot position and controlled range."),
    _exercise("Calves", CALF_SOLEUS, "Seated Calf Raise Machine", "Machine", "Isolation", "bent_knee_calf", "12-20", "Bent-knee calf raises relatively emphasise soleus because the gastrocnemius crosses the knee.", "Keep knees comfortably bent and pause without bouncing."),
    _exercise("Calves", CALF_SOLEUS, "Seated Dumbbell Calf Raise", "Dumbbells", "Isolation", "bent_knee_calf", "12-20", "A dumbbell placed securely over the thighs can load seated calf raises.", "Use padding and avoid placing load directly on the kneecap."),

    # CORE: trunk flexion, rotation/anti-rotation and anti-extension.
    _exercise("Core", CORE_ABS, "Cable Crunch", "Cable", "Isolation", "trunk_flexion", "10-15", "A cable crunch loads trunk flexion for the rectus abdominis.", "Curl the ribcage toward the pelvis rather than pulling with the arms."),
    _exercise("Core", CORE_ABS, "Ab Crunch Machine", "Machine", "Isolation", "trunk_flexion", "10-15", "The machine provides adjustable resistance for trunk flexion.", "Set the machine to your body and move without jerking."),
    _exercise("Core", CORE_ABS, "Reverse Crunch", "Bodyweight", "Isolation", "reverse_crunch", "10-15", "A reverse crunch uses posterior pelvic tilt and trunk control to train the abdominal wall.", "Lift the pelvis smoothly; avoid swinging the legs."),
    _exercise("Core", CORE_ABS, "Decline Sit-Up", "Bodyweight", "Compound", "sit_up", "8-12", "A sit-up combines trunk flexion and hip flexion and involves the abdominal muscles and hip flexors.", "Use a comfortable range and avoid pulling the neck."),
    _exercise("Core", CORE_OBLIQUES, "Cable Woodchop", "Cable", "Compound", "woodchop", "10-12 each side", "A woodchop trains controlled trunk rotation involving the obliques and other trunk muscles.", "Rotate through the trunk and hips together without yanking the cable."),
    _exercise("Core", CORE_OBLIQUES, "Pallof Press", "Cable", "Stability", "anti_rotation", "10-12 each side", "A Pallof press challenges the obliques and trunk to resist rotation.", "Keep hips and shoulders square as arms extend."),
    _exercise("Core", CORE_OBLIQUES, "Band Pallof Press", "Resistance Band", "Stability", "anti_rotation", "10-12 each side", "A band Pallof press is a home or gym alternative for anti-rotation work.", "Anchor the band securely and move slowly."),
    _exercise("Core", CORE_OBLIQUES, "Side Plank", "Bodyweight", "Stability", "side_plank", "20-40 seconds each side", "A side plank challenges the obliques and lateral trunk stabilisers.", "Keep hips stacked and shorten the lever by bending knees if needed."),
    _exercise("Core", CORE_STABILITY, "Plank", "Bodyweight", "Stability", "plank", "20-45 seconds", "A plank trains the trunk to resist extension.", "Keep a straight line from head to heels and breathe steadily."),
    _exercise("Core", CORE_STABILITY, "Dead Bug", "Bodyweight", "Stability", "dead_bug", "8-12 each side", "A dead bug trains trunk control while arms and legs move.", "Keep the lower back position steady without holding your breath."),
    _exercise("Core", CORE_STABILITY, "Ab Wheel Rollout", "Bodyweight", "Compound", "ab_wheel", "6-10", "An ab-wheel rollout challenges the abdominal wall to resist spinal extension.", "Start with a short range and stop before the lower back arches."),

    # TRAPS: upper, middle and lower regions of the trapezius.
    _exercise("Traps", TRAP_UPPER, "Barbell Shrug", "Barbell", "Isolation", "shrug", "8-12", "Shrugs train shoulder-blade elevation with upper-trapezius emphasis.", "Move shoulders upward smoothly; do not roll them in circles."),
    _exercise("Traps", TRAP_UPPER, "Dumbbell Shrug", "Dumbbells", "Isolation", "shrug", "10-15", "Dumbbell shrugs are a simple alternative for upper-trap work.", "Pause briefly at the top and lower under control."),
    _exercise("Traps", TRAP_UPPER, "Cable Shrug", "Cable", "Isolation", "shrug", "10-15", "Cable shrugs provide continuous resistance for shoulder-blade elevation.", "Keep arms long and avoid leaning back."),
    _exercise("Traps", TRAP_UPPER, "Farmer Carry", "Dumbbells", "Compound", "farmer_carry", "20-40 metres", "A loaded carry challenges grip, trunk and upper-trap stabilisation.", "Walk tall with controlled steps and a load you can hold safely."),
    _exercise("Traps", TRAP_MIDDLE, "Chest-Supported Row", "Machine", "Compound", "trap_row", "8-12", "A row with controlled shoulder-blade retraction involves middle traps and rhomboids.", "Avoid shrugging; let the shoulder blades move naturally."),
    _exercise("Traps", TRAP_MIDDLE, "Seated Cable Row", "Cable", "Compound", "trap_row", "8-12", "A cable row trains scapular retractors along with lats and arm muscles.", "Keep torso steady and avoid jerking the handle."),
    _exercise("Traps", TRAP_MIDDLE, "Prone T Raise", "Dumbbells", "Isolation", "prone_t_raise", "10-15", "A light T raise challenges middle-trap and rear-shoulder control.", "Use very light weights and keep neck relaxed."),
    _exercise("Traps", TRAP_LOWER, "Incline Bench Y Raise", "Dumbbells", "Isolation", "trap_y_raise", "10-15", "A Y raise is a low-load option for lower-trap contribution to shoulder-blade control.", "Use a very light load and avoid shrugging toward the ears."),
    _exercise("Traps", TRAP_LOWER, "Cable Y Raise", "Cable", "Isolation", "trap_y_raise", "10-15", "The cable Y raise trains lower-trap-oriented shoulder-blade movement.", "Move smoothly and stop if the shoulder feels uncomfortable."),

    # FOREARMS: elbow flexion support, wrist flexion and extension.
    _exercise("Forearms", FOREARM_BRACHIO, "Dumbbell Hammer Curl", "Dumbbells", "Isolation", "forearm_hammer", "8-12", "The neutral grip involves brachioradialis as an elbow flexor.", "Keep wrists neutral and avoid swinging."),
    _exercise("Forearms", FOREARM_BRACHIO, "Reverse EZ-Bar Curl", "Barbell", "Isolation", "forearm_reverse_curl", "10-15", "A reverse curl places more demand on brachioradialis and other forearm muscles.", "Choose a lighter load and keep elbows still."),
    _exercise("Forearms", FOREARM_BRACHIO, "Rope Hammer Curl", "Cable", "Isolation", "forearm_hammer", "10-15", "A rope hammer curl is a cable option for neutral-grip elbow flexion.", "Keep elbows close and control the lowering phase."),
    _exercise("Forearms", FOREARM_FLEXORS, "Seated Wrist Curl", "Dumbbells", "Isolation", "wrist_curl", "12-20", "Wrist curls train wrist flexors through controlled wrist flexion.", "Support forearms and use a light weight."),
    _exercise("Forearms", FOREARM_FLEXORS, "Farmer Carry", "Dumbbells", "Compound", "forearm_carry", "20-40 metres", "Loaded carries challenge grip and forearm endurance.", "Use a load that allows an upright walk without losing grip suddenly."),
    _exercise("Forearms", FOREARM_EXTENSORS, "Reverse Wrist Curl", "Dumbbells", "Isolation", "reverse_wrist_curl", "12-20", "Reverse wrist curls train the wrist extensors.", "Support forearms and move through a small, controlled range."),
    _exercise("Forearms", FOREARM_EXTENSORS, "Band Wrist Extension", "Resistance Band", "Isolation", "reverse_wrist_curl", "15-20", "A band is a light option for wrist extension work.", "Use low tension and avoid snapping the wrist."),

    # ADDUCTORS: inner-thigh strength and hip control.
    _exercise("Adductors", ADDUCTOR_FOCUS, "Seated Hip Adduction Machine", "Machine", "Isolation", "hip_adduction", "10-15", "The adduction machine trains the inner-thigh muscles bringing the legs together.", "Use a comfortable range and avoid bouncing the pads."),
    _exercise("Adductors", ADDUCTOR_FOCUS, "Standing Cable Hip Adduction", "Cable", "Isolation", "hip_adduction", "10-15 each side", "A cable adduction works one leg at a time through hip adduction.", "Hold a stable support and keep the pelvis facing forward."),
    _exercise("Adductors", ADDUCTOR_FOCUS, "Side-Lying Hip Adduction", "Bodyweight", "Isolation", "hip_adduction_bodyweight", "10-15 each side", "A side-lying adduction is a no-equipment inner-thigh exercise.", "Lift the lower leg smoothly without rolling the hips."),
    _exercise("Adductors", ADDUCTOR_FOCUS, "Copenhagen Side Plank (easy lever)", "Bodyweight", "Stability", "copenhagen_plank", "10-20 seconds each side", "A Copenhagen plank challenges the adductors and trunk as a stability exercise.", "Begin with the knee supported on a bench and progress gradually."),
]


def get_focus_options(muscle_group):
    """Return anatomical focus options for the selected muscle group."""
    return list(FOCUS_GUIDE.get(muscle_group, {}).keys())


def get_focus_education(muscle_group, focus):
    """Return plain-language anatomy notes for a selected focus."""
    return FOCUS_GUIDE.get(muscle_group, {}).get(
        focus,
        {
            "summary": "Choose a focus area to see which muscles and movement patterns are involved.",
            "limitation": "Exercise selection changes emphasis; it does not perfectly isolate a single muscle.",
        },
    )


def _exercise_count_for_time(minutes):
    if minutes <= 20:
        return 3
    if minutes <= 30:
        return 4
    if minutes <= 45:
        return 5
    return 6


def _select_distinct_patterns(candidates, count):
    """Choose a varied list, preferring compounds before isolation work."""
    selected = []
    used_patterns = set()

    def add_from(pool):
        for item in pool:
            if item["pattern"] not in used_patterns:
                selected.append(item)
                used_patterns.add(item["pattern"])
                return True
        return False

    compounds = [x for x in candidates if x["movement_type"] == "Compound"]
    isolations = [x for x in candidates if x["movement_type"] == "Isolation"]
    stability = [x for x in candidates if x["movement_type"] == "Stability"]

    # Alternate movement types so a session is not only presses/rows or only curls/flys.
    pools = [compounds, isolations, compounds, isolations, stability, compounds, isolations]
    while len(selected) < count:
        added = False
        for pool in pools:
            if len(selected) >= count:
                break
            if add_from(pool):
                added = True
        if not added:
            break
    return selected


def generate_workout(
    experience,
    goal,
    minutes,
    muscle_group="Chest",
    focus="All areas",
    unavailable_equipment=None,
):
    """Generate a muscle-group session with transparent head/region emphasis.

    Bodyweight entries are always retained; the busy-equipment selector only
    filters equipment listed in EQUIPMENT_OPTIONS.
    """
    unavailable = set(unavailable_equipment or [])
    allowed_focuses = get_focus_options(muscle_group)
    if not allowed_focuses:
        return []
    if focus != "All areas" and focus not in allowed_focuses:
        return []

    candidates = [
        item for item in EXERCISES
        if item["muscle"] == muscle_group
        and (item["equipment"] == "Bodyweight" or item["equipment"] not in unavailable)
    ]

    # If a specific head/region is selected, include direct emphasis exercises
    # and appropriate compound/supporting movements that also train it.
    if focus != "All areas":
        candidates = [
            item for item in candidates
            if item["focus"] == focus or focus in item["supports"]
        ]

        direct = [item for item in candidates if item["focus"] == focus]
        supporting = [item for item in candidates if item["focus"] != focus]
        direct_compounds = [x for x in direct if x["movement_type"] == "Compound"]
        support_compounds = [x for x in supporting if x["movement_type"] == "Compound"]
        direct_isolations = [x for x in direct if x["movement_type"] == "Isolation"]
        support_isolations = [x for x in supporting if x["movement_type"] == "Isolation"]
        stability = [x for x in candidates if x["movement_type"] == "Stability"]

        # Prioritise a relevant compound lift, then direct focus work.
        ordered = []
        for pool in (direct_compounds, support_compounds, direct_isolations, support_isolations, stability):
            ordered.extend(pool)
        candidates = ordered
    else:
        # For a whole muscle group, round-robin through focus labels so that
        # longer sessions are more likely to cover more than one region.
        grouped = {}
        for item in candidates:
            grouped.setdefault(item["focus"], []).append(item)
        ordered = []
        for focus_name, entries in grouped.items():
            ordered.extend([x for x in entries if x["movement_type"] == "Compound"])
            ordered.extend([x for x in entries if x["movement_type"] == "Isolation"])
            ordered.extend([x for x in entries if x["movement_type"] == "Stability"])
        candidates = ordered

    # One variation per movement pattern avoids suggesting several near-identical
    # versions in the same session. Alternatives remain visible for substitution.
    selected = _select_distinct_patterns(candidates, _exercise_count_for_time(int(minutes)))

    if experience == "Beginner":
        sets_count = 2
    elif experience == "Advanced":
        sets_count = 3
    else:
        sets_count = 3

    workout_plan = []
    for item in selected:
        alternatives = [
            f'{option["name"]} ({option["equipment"]})'
            for option in candidates
            if option["pattern"] == item["pattern"]
            and option["name"] != item["name"]
        ]
        # Remove duplicate alternative names while preserving order.
        alternatives = list(dict.fromkeys(alternatives))
        workout_plan.append({
            **item,
            "sets": sets_count,
            "goal": goal,
            "alternatives": alternatives,
        })

    return workout_plan
