from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    email = Column(String(100), unique=True)
    is_admin = Column(Integer, default=0)
    reservations = relationship('Reservation', back_populates='user')
    def has_overlapping_reservation(self, room_id, check_in_date, check_out_date):
        """
        Check if the user has overlapping reservations for a given room and date range.
        """
        overlapping_reservations = [
            reservation for reservation in self.reservations
            if (
                reservation.room_id == room_id and
                reservation.check_out_date > check_in_date and
                reservation.check_in_date < check_out_date
            )
        ]
        return bool(overlapping_reservations)


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String(10), unique=True)
    room_type = Column(String(50))
    price = Column(Integer)
    availability = Column(Integer, default=1)
    reservations = relationship('Reservation', back_populates='room')
    def is_available(self, check_in_date, check_out_date):
        # Check if the room is available for the given dates
        reservations = Reservation.query.filter(
            Room.id == self.id,
            (
                (Reservation.check_in_date <= check_in_date)
                & (Reservation.check_out_date >= check_in_date)
            )
            | (
                (Reservation.check_in_date <= check_out_date)
                & (Reservation.check_out_date >= check_out_date)
            )
        ).all()

        return not reservations
    def has_overlapping_reservation(self, room_id, check_in_date, check_out_date):
        """
        Check if the user has overlapping reservations for a specific room and date range.
        """
        overlapping_reservation = Reservation.query.filter(
            Reservation.user_id == self.id,
            Reservation.room_id == room_id,
            Reservation.check_in_date < check_out_date,
            Reservation.check_out_date > check_in_date
        ).first()

        return overlapping_reservation is not None


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    check_in_date = Column(DateTime, default=datetime.utcnow)
    check_out_date = Column(DateTime)
    user = relationship('User', back_populates='reservations')
    room = relationship('Room', back_populates='reservations')
