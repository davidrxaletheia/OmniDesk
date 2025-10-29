"""CLI pequeño: pedir login y mostrar métricas generales de la plataforma.

Ejecutar desde la raíz del repo:
	python python/dashboard.py

El script pedirá usuario/email y contraseña (oculta), usará
`singUp.authenticate` y, si la autenticación es correcta, imprimirá
resúmenes (counts) usando los repos existentes.
"""

from __future__ import annotations

import os
import sys
from getpass import getpass
from typing import Optional

# Asegura que el paquete `Classes` sea importable cuando se ejecuta desde la raíz
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

try:
	import singUp
except Exception:
	# también permitir import relativo si se ejecuta desde python/ directamente
	try:
		sys.path.insert(0, os.getcwd())
		import singUp
	except Exception as e:
		print('No se pudo importar singUp:', e)
		raise

from Classes.repos.app_user_repo import AppUserRepo
from Classes.repos.ticket_repo import TicketRepo
from Classes.repos.client_repo import ClientRepo
from Classes.repos.product_repo import ProductRepo
from Classes.repos.order_repo import CustomerOrderRepo
from Classes.repos.calendar_repo import CalendarEventRepo


def scalar_count(repo, where: Optional[str]=None, params: tuple=()):
	"""Run SELECT COUNT(*) against repo.table with optional WHERE."""
	db = repo.db
	cur = db.cursor()
	if where:
		sql = f"SELECT COUNT(*) FROM {repo.table} WHERE {where}"
		cur.execute(sql, params)
	else:
		sql = f"SELECT COUNT(*) FROM {repo.table}"
		cur.execute(sql)
	row = cur.fetchone()
	return row[0] if row else 0


def show_summary():
	# instantiate repos
	urepo = AppUserRepo()
	trepo = TicketRepo()
	crepo = ClientRepo()
	prepo = ProductRepo()
	orepo = CustomerOrderRepo()
	try:
		total_users = scalar_count(urepo)
		active_users = scalar_count(urepo, 'active=%s', (True,))
		open_tickets = scalar_count(trepo, "status IN ('abierto','en_progreso')")
		total_clients = scalar_count(crepo)
		total_products = scalar_count(prepo)
		total_orders = scalar_count(orepo)

		print('\n--- Resumen de la plataforma ---')
		print(f'Total usuarios:       {total_users}')
		print(f'Usuarios activos:     {active_users}')
		print(f'Tickets abiertos:     {open_tickets}')
		print(f'Total clientes:       {total_clients}')
		print(f'Total productos:      {total_products}')
		print(f'Total pedidos:        {total_orders}')
		print('-------------------------------\n')

	finally:
		try: urepo.close()
		except: pass
		try: trepo.close()
		except: pass
		try: crepo.close()
		except: pass
		try: prepo.close()
		except: pass
		try: orepo.close()
		except: pass


def show_calendar(month_offset: int = 0):
	"""Print a simple ASCII calendar for the current month (offset allowed)
	and list events grouped by day. """
	import calendar as _calendar
	from datetime import date, datetime, timedelta

	today = date.today()
	# compute target month/year with offset
	year = today.year
	month = today.month + month_offset
	while month < 1:
		month += 12
		year -= 1
	while month > 12:
		month -= 12
		year += 1

	# fetch upcoming events and keep those in the target month
	crepo = CalendarEventRepo()
	try:
		events = crepo.upcoming(limit=200)
	finally:
		try: crepo.close()
		except: pass

	# group events by day
	events_by_day = {}
	for ev in events:
		# ev.start_time is datetime
		ev_date = ev.start_time.date()
		if ev_date.year == year and ev_date.month == month:
			events_by_day.setdefault(ev_date.day, []).append(ev)

	cal = _calendar.TextCalendar(_calendar.MONDAY)
	cal_lines = cal.formatmonth(year, month).splitlines()

	# we will inject markers for days that have events (append *)
	def mark_day_token(token):
		try:
			d = int(token)
		except Exception:
			return token
		# if any event that day is linked to a ticket, mark with 'T' instead
		day_events = events_by_day.get(d)
		if day_events:
			has_ticket = any(getattr(e, 'ticket_id', None) for e in day_events)
			if has_ticket:
				return "T"
			return f"{token}*"
		return token

	# print header and modify the calendar body lines
	print(f"\nCalendario — {year}-{month:02d}")
	for i, line in enumerate(cal_lines):
		if i < 2:
			print(line)
			continue
		# replace each day token with marked version keeping spacing
		parts = line.split()
		new_parts = [mark_day_token(p) for p in parts]
		# rebuild line with spacing similar to original (join with single space)
		print(' '.join(new_parts))

	# list events under calendar
	if not events_by_day:
		print('\nNo hay eventos en este mes.')
		return

	print('\nEventos:\n')
	# prepare ticket repo to fetch ticket details when available
	trepo = TicketRepo()
	try:
		for day in sorted(events_by_day.keys()):
			print(f"{year}-{month:02d}-{day:02d}:")
			for ev in sorted(events_by_day[day], key=lambda e: e.start_time):
				st = ev.start_time.strftime('%H:%M')
				et = ev.end_time.strftime('%H:%M') if getattr(ev, 'end_time', None) else ''
				title = getattr(ev, 'title', '')
				if getattr(ev, 'ticket_id', None):
					ticket = trepo.get(ev.ticket_id)
					tinfo = f" [Ticket id={ev.ticket_id} subject='{getattr(ticket, 'subject', '')}' status={getattr(ticket, 'status', '')}]"
				else:
					tinfo = ''
				print(f"  - {st}-{et} {title} (id={ev.event_id}){tinfo}")
	finally:
		try: trepo.close()
		except: pass



def main():
	print('Bienvenido al CLI de Dashboard')
	identifier = input('Usuario o email: ').strip()
	password = getpass('Contraseña: ')

	user = singUp.authenticate(identifier, password)
	if not user:
		print('Autenticación fallida. Saliendo.')
		return

	print(f'Autenticación OK. Bienvenido, {user.full_name} (role={user.role})')
	show_summary()
	show_calendar()


if __name__ == '__main__':
	main()

