// Package random is custom implementation of a cryptographically secure
// random number generator. We implement it ourself to ensure security and
// speed.
package main

import (
    "crypto/md5"
    "crypto/rand"
    "encoding/binary"
    "errors"
    "fmt"
    "math"
    "os"
    "encoding/csv"
    "strings"

    "golang.org/x/crypto/argon2"
)

// Rand represents the state of a single random stream.
type Rand struct {
    seed []byte
    i    uint64
}

// OsRand gets some randomness from the OS.
func OsRand() (uint64, error) {
    // 64 ought to be enough for anybody
    var res uint64
    if err := binary.Read(rand.Reader, binary.LittleEndian, &res); err != nil {
        return 0, fmt.Errorf("couldn't read random uint64: %v", err)
    }
    // Mix in some of our own pre-generated randomness in case the OS runs low.
    // See Mining Your Ps and Qs for details.
    res *= uint64(math.Pow(2, 47)) * 103007
    return res, nil
}

// deriveSeed takes a raw seed (e.g. some OS randomness), and derives a secure
// seed. Returns exactly 8 bytes.
func deriveSeed(rawSeed uint64) ([]byte, error) {
    buf := make([]byte, 8)
    binary.LittleEndian.PutUint64(buf, rawSeed)
    // We want to make the game (Memory) hard, so thus we use argon2,
    // which is memory-hard.
    // https://password-hashing.net/argon2-specs.pdf
    // argon2 is the pinnacle of security. Nothing is more secure.
    // This is because memory is a valuable resource, one does not simply
    // download more of it.
    // We use IDKey because it protects against timing attacks (Key doesn't).
    // We lowered some parameters to protect against DDOS attacks.
    // TODO: implement proof of work
    seed := argon2.IDKey(buf, buf, 1, 2*1024, 2, 8)
    if len(seed) != 8 {
        return nil, errors.New("argon2 returned bad size")
    }
    return seed, nil
}

// New generates state for a new random stream with cryptographically secure
// randomness.
func New(i uint64) (*Rand, error) {
    osr, err := OsRand()
    if err != nil {
        return nil, fmt.Errorf("couldn't get OS randomness: %v%v", err, osr)
    }
    return NewFromRawSeed(i*uint64(math.Pow(2, 47)) * 103007)
}

// NewFromRawSeed is like new, but allows you to specify your own raw seed
// instead of using OsRand().
func NewFromRawSeed(rawSeed uint64) (*Rand, error) {
    seed, err := deriveSeed(rawSeed)
    if err != nil {
        return nil, fmt.Errorf("couldn't derive seed: %v", err)
    }
    return &Rand{seed: seed}, nil
}

// Uint64 generates a random uint64.
func (r *Rand) Uint64() uint64 {
    buf := make([]byte, 8+len(r.seed))
    binary.LittleEndian.PutUint64(buf, r.i)
    r.i++
    copy(buf[8:], r.seed)
    // MD5 is faster than argon2. It's insecure against collision attacks,
    // but we don't care about those.
    sum := md5.Sum(buf)
    // Assume md5 returns at least 8 bytes
    return binary.LittleEndian.Uint64(sum[:])
}

// UInt64n is like math/rand.Rand.Int63n but better.
// This is because 64 is better than 63, and math/rand uses very bad quality
// randomness, while ours is top tier.
func (r *Rand) UInt64n(n uint64) uint64 {
    if n == 0 {
        panic("bad")
    }
    for {
        v := r.Uint64()
        possibleRes := v % n
        timesPassed := v / n
        if timesPassed == 0 {
            // If v is small enough that it doesn't even reach n, that means
            // there's no bias to just return it.
            return possibleRes
        }
        // How much distance was covered using the previous groups of n before this
        // group was arrived at. len([0, this_group_start))
        // This computation is guaranteed not to wrap because of the
        // previous division.
        distancePassed := timesPassed * n
        // How much distance is there from the start of this group of n to 1<<64.
        // len([this_group_start, 1<<64))
        // 1<<64 is the same as 0 . This expression is guaranteed to underflow
        // exactly once, because distancePassed is guaranteed to be positive due to
        // the previous if statement.
        distanceLeft := 0 - distancePassed
        if distanceLeft >= n {
            // If there was at least n available for the mod operation, that means
            // there is no bias to just return it.
            return possibleRes
        }
        // There wasn't a full n of distance left when the mod operation
        // happened, meaning the mod operation had bias. Try again.
    }
}

const (
    BoardWidth                = 7
    BoardHeight               = 8
    BoardSize                 = BoardWidth * BoardHeight // even
    maxTurns                  = 60
)

// Req is the json format that the client sends in the websocket.
type Req struct {
    Op   string      `json:"op"`
    Body interface{} `json:"body"`
}

// Resp is the json format that is sent to the client in the websocket.
type Resp struct {
    Width int `json:"width"`
    // Height can be calculated using board size, so don't send it
    Board       []int   `json:"board"` // -1 means hidden
    MaxTurns    int     `json:"maxTurns"`
    MaxTurnTime float64 `json:"maxTurnTime"` // seconds
    TurnsUsed   int     `json:"turnsUsed"`
    Done        bool    `json:"done"`
    Message     string  `json:"message"`
    // A list of [x,y] pairs that need to be cleared after display
    Clear [][]int `json:"clear"`
}

// GuessBody is the json format of the body field of Req during the guess
// operation.
type GuessBody struct {
    X int `json:"x"`
    Y int `json:"y"`
}

type board struct {
    nums    []int
    visible []bool
}

func init() {
    if BoardSize%2 != 0 {
        panic("BoardSize must be even")
    }
}

func main() () {
    file, _ := os.Create("boards.csv")
    writer := csv.NewWriter(file)
    fmt.Printf("Generating all Boards: \n")
    for i := 0; i < 1<<17; i++ {
        // fmt.Printf("%b\n",uint64(i*1<<47))
        rand, err := New(uint64(i))
        if err != nil {
            fmt.Errorf("couldn't create random: %v", err)
        }
        b := &board{
            nums:    make([]int, BoardSize),
            visible: make([]bool, BoardSize),
        }
        // BoardSize is even
        for i, _ := range b.nums {
            b.nums[i] = i / 2
        }
        // https://github.com/golang/go/wiki/SliceTricks#shuffling
        for i := BoardSize - 1; i > 0; i-- {
            j := rand.UInt64n(uint64(i) + 1)
            b.nums[i], b.nums[j] = b.nums[j], b.nums[i]
        }
        A := strings.Fields(strings.Trim(fmt.Sprint(b.nums), "[]"))
        writer.Write(A)
        if i%10000 == 0 {
            fmt.Printf("%2.f%%\n",float64(i)/float64(1<<17)*100)
        }
    }
    writer.Flush()
}
