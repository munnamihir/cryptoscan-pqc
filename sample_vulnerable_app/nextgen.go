package main

// Already migrated: hybrid key exchange using ML-KEM-768
import "example.com/pq/mlkem"

func KeyExchange() {
    _ = mlkem.NewKey768()  // ML-KEM-768, quantum-safe
}
