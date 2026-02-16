"""
Django management command to seed development database with dummy data.
Run this after migrations: python manage.py seed_dev_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import random

from backend_api.models import (
    Todo, Person, PartTimer, Role, CollegesList, CollegeDetail,
    AccessRoles, Employer, Recruiter, Consultant, StatusConsultant,
    User, Package, AcsParttimerStatus, StatusUpdates, ShopingProduct,
    TeamMember, DeviceAllocation, HappinessIndex, Subsidiary
)
from transaction_api.models import Transaction


class Command(BaseCommand):
    help = 'Seed development database with dummy data (10-30 records per model)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self._clear_data()

        self.stdout.write(self.style.SUCCESS('Starting to seed dummy data...'))

        # Seed in dependency order
        self._seed_subsidiaries()
        self._seed_access_roles()
        self._seed_users()
        self._seed_employers()
        self._seed_recruiters()
        self._seed_consultants()
        self._seed_status_consultants()
        self._seed_roles()
        self._seed_packages()
        self._seed_colleges()
        self._seed_college_details()
        self._seed_persons()
        self._seed_part_timers()
        self._seed_todos()
        self._seed_acs_parttimer_status()
        self._seed_status_updates()
        self._seed_transactions()
        self._seed_team_members()
        self._seed_device_allocations()
        self._seed_happiness_indexes()
        self._seed_shopping_products()

        self.stdout.write(self.style.SUCCESS('Successfully seeded all dummy data!'))

    def _clear_data(self):
        """Clear all data from models"""
        models_to_clear = [
            ShopingProduct, HappinessIndex, DeviceAllocation, TeamMember,
            Transaction, StatusUpdates, AcsParttimerStatus, Todo,
            PartTimer, Person, CollegeDetail, CollegesList,
            StatusConsultant, Consultant, Role, Package, Recruiter,
            Employer, User, AccessRoles, Subsidiary
        ]
        for model in models_to_clear:
            count = model.objects.all().count()
            model.objects.all().delete()
            self.stdout.write(f'  Deleted {count} {model.__name__} records')

    def _seed_subsidiaries(self):
        """Seed Subsidiary model"""
        subsidiaries = [
            {'subsidiaryName': 'AMS', 'subName': 'Anddhen Management Services', 'parttimer_multi_status': True, 'active': True},
            {'subsidiaryName': 'ACS', 'subName': 'Anddhen Consulting Services', 'parttimer_multi_status': False, 'active': True},
            {'subsidiaryName': 'ASS', 'subName': 'Anddhen Software Services', 'parttimer_multi_status': True, 'active': True},
            {'subsidiaryName': 'APS', 'subName': 'Anddhen Professional Services', 'parttimer_multi_status': False, 'active': True},
            {'subsidiaryName': 'ATI', 'subName': 'Anddhen Technology Inc', 'parttimer_multi_status': True, 'active': True},
        ]
        for data in subsidiaries:
            Subsidiary.objects.get_or_create(subsidiaryName=data['subsidiaryName'], defaults=data)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(subsidiaries)} Subsidiary records'))

    def _seed_access_roles(self):
        """Seed AccessRoles model"""
        roles = [
            {'admin_access_role': 'super_admin', 'name_of_role': 'Super Administrator'},
            {'admin_access_role': 'admin', 'name_of_role': 'Administrator'},
            {'admin_access_role': 'manager', 'name_of_role': 'Manager'},
            {'admin_access_role': 'employee', 'name_of_role': 'Employee'},
            {'admin_access_role': 'consultant', 'name_of_role': 'Consultant'},
            {'admin_access_role': 'recruiter', 'name_of_role': 'Recruiter'},
        ]
        for role_data in roles:
            AccessRoles.objects.get_or_create(admin_access_role=role_data['admin_access_role'], defaults=role_data)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(roles)} AccessRoles records'))

    def _seed_users(self):
        """Seed User model"""
        first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry',
                      'Ivy', 'Jack', 'Kate', 'Liam', 'Mia', 'Noah', 'Olivia', 'Paul', 'Quinn', 'Rachel',
                      'Steve', 'Tina', 'Uma', 'Victor', 'Wendy', 'Xander', 'Yara', 'Zoe']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        users = []
        for i in range(25):
            first = random.choice(first_names)
            last = random.choice(last_names)
            user_id = f'user_{i+1:03d}'
            email = f'{first.lower()}.{last.lower()}@example.com'
            
            users.append(User(
                user_id=user_id,
                full_name=f'{first} {last}',
                first_name=first,
                last_name=last,
                phone_country_code='+1',
                phone_number=f'{random.randint(2000000000, 9999999999)}',  # 10 digits only (no dashes)
                email_id=email,
                enrolled_services=['service1', 'service2'] if i % 2 == 0 else ['service3']
            ))
        User.objects.bulk_create(users, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(users)} User records'))

    def _seed_employers(self):
        """Seed Employer model"""
        employers = [
            {'name': 'Tech Corp Inc', 'address': '123 Tech Street, San Francisco, CA 94105'},
            {'name': 'Global Solutions LLC', 'address': '456 Business Ave, New York, NY 10001'},
            {'name': 'Innovation Systems', 'address': '789 Innovation Blvd, Austin, TX 78701'},
            {'name': 'Digital Dynamics', 'address': '321 Digital Way, Seattle, WA 98101'},
            {'name': 'Cloud Services Co', 'address': '654 Cloud Drive, Boston, MA 02101'},
            {'name': 'Data Analytics Inc', 'address': '987 Data Lane, Denver, CO 80201'},
            {'name': 'Software Solutions', 'address': '147 Software Street, Atlanta, GA 30301'},
            {'name': 'AI Technologies', 'address': '258 AI Avenue, Portland, OR 97201'},
        ]
        for emp_data in employers:
            Employer.objects.get_or_create(name=emp_data['name'], defaults=emp_data)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(employers)} Employer records'))

    def _seed_recruiters(self):
        """Seed Recruiter model"""
        employers = list(Employer.objects.all())
        if not employers:
            return
            
        recruiter_names = ['Sarah Johnson', 'Mike Chen', 'Lisa Park', 'David Kim', 'Emma Wilson',
                          'James Brown', 'Olivia Martinez', 'Robert Taylor', 'Sophia Anderson', 'Michael Thomas']
        
        recruiters = []
        for i, name in enumerate(recruiter_names[:15]):
            recruiter_data = {
                'name': name,
                'phone': f'{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}',
                'employer': random.choice(employers).name,
                'email': f'{name.lower().replace(" ", ".")}@example.com'
            }
            recruiter, created = Recruiter.objects.get_or_create(phone=recruiter_data['phone'], defaults=recruiter_data)
            if created:
                recruiters.append(recruiter)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(recruiters)} Recruiter records'))

    def _seed_consultants(self):
        """Seed Consultant model"""
        employers = list(Employer.objects.all())
        recruiters = list(Recruiter.objects.all())
        if not employers or not recruiters:
            return

        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 'Cameron', 'Dakota']
        last_names = ['Patel', 'Singh', 'Kumar', 'Sharma', 'Reddy', 'Mehta', 'Gupta', 'Verma', 'Agarwal', 'Jain']
        visa_statuses = ['OPT', 'CPT', 'H1B', 'H4 EAD']
        technologies_list = [['Python', 'Django'], ['Java', 'Spring'], ['React', 'Node.js'], ['Angular', 'TypeScript'],
                           ['C#', '.NET'], ['Go', 'Docker'], ['Ruby', 'Rails'], ['PHP', 'Laravel']]

        consultants = []
        for i in range(20):
            first = random.choice(first_names)
            last = random.choice(last_names)
            consultant = Consultant(
                employer_id=random.choice(employers),
                recruiter_id=random.choice(recruiters) if i % 2 == 0 else None,
                full_name=f'{first} {last}',
                full_name_verified=random.choice([True, False]),
                phone_number=f'{random.randint(200,999)}{random.randint(100,999)}{random.randint(1000,9999)}',
                email_id=f'{first.lower()}.{last.lower()}@consultant.com',
                dob=date(1990, 1, 1) + timedelta(days=random.randint(0, 10000)),
                visa_status=random.choice(visa_statuses),
                visa_status_verified=random.choice([True, False]),
                visa_validity=timezone.now().date() + timedelta(days=random.randint(30, 1095)),
                visa_validity_verified=random.choice([True, False]),
                btech_college=f'University {i+1}' if i % 3 != 0 else None,
                btech_percentage=Decimal(f'{random.randint(70, 95)}.{random.randint(10, 99)}') if i % 3 != 0 else None,
                btech_graduation_date=date(2015, 6, 1) + timedelta(days=random.randint(0, 1825)) if i % 3 != 0 else None,
                masters_college=f'Graduate University {i+1}' if i % 2 == 0 else None,
                masters_cgpa=Decimal(f'{random.randint(3, 4)}.{random.randint(0, 9)}') if i % 2 == 0 else None,
                masters_graduation_date=date(2018, 5, 1) + timedelta(days=random.randint(0, 1825)) if i % 2 == 0 else None,
                technologies=random.choice(technologies_list),
                current_location=random.choice(['San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA', 'Boston, MA']),
                relocation=random.choice([True, False]),
                experience_in_us=f'{random.randint(1, 10)} years in software development',
                experience_in_us_verified=random.choice([True, False]),
                experience_in_india=f'{random.randint(0, 5)} years in software development' if i % 2 == 0 else '',
                experience_in_india_verified=random.choice([True, False]) if i % 2 == 0 else False,
                relocation_preference=random.choice(['Any', 'West Coast', 'East Coast', 'Remote']) if i % 3 == 0 else None,
                passport_number=f'A{random.randint(1000000, 9999999)}' if i % 2 == 0 else '',
                passport_number_verified=random.choice([True, False]) if i % 2 == 0 else False,
                driving_licence=f'DL{random.randint(100000, 999999)}' if i % 3 == 0 else '',
                rate_expectations=f'${random.randint(60, 150)}/hr' if i % 2 == 0 else None,
                last_4_ssn=f'{random.randint(1000, 9999)}' if i % 4 == 0 else None,
                linkedin_url=f'https://linkedin.com/in/{first.lower()}-{last.lower()}-{i}',
                linkedin_url_verified=random.choice([True, False]),
                uploaded_date=timezone.now().date() - timedelta(days=random.randint(0, 365))
            )
            consultants.append(consultant)

        Consultant.objects.bulk_create(consultants, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(consultants)} Consultant records'))

    def _seed_status_consultants(self):
        """Seed StatusConsultant model"""
        consultants = list(Consultant.objects.all())
        recruiters = list(Recruiter.objects.all())
        employers = list(Employer.objects.all())
        
        if not consultants:
            return

        statuses = []
        for i in range(15):
            days_ago = random.randint(0, 90)
            status_date = timezone.now().date() - timedelta(days=days_ago)
            statuses.append(StatusConsultant(
                consultant_id=random.choice(consultants),
                recruiter_id=random.choice(recruiters) if recruiters else None,
                employer_id=random.choice(employers) if employers else None,
                date=status_date,
                description=f'Status update for consultant on {status_date}: Working on project assignment.'
            ))

        StatusConsultant.objects.bulk_create(statuses, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(statuses)} StatusConsultant records'))

    def _seed_roles(self):
        """Seed Role model"""
        users = list(User.objects.all())
        access_roles = list(AccessRoles.objects.all())
        
        if not users or not access_roles:
            return

        roles = []
        for i in range(20):
            user = random.choice(users)
            access_role = random.choice(access_roles)
            roles.append(Role(
                user_id=user.user_id,
                name=user.full_name or f'User {i+1}',
                role_name=access_role.name_of_role
            ))

        Role.objects.bulk_create(roles, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(roles)} Role records'))

    def _seed_packages(self):
        """Seed Package model"""
        packages_data = [
            {
                'package_name': 'Basic Package',
                'includes': ['Service 1', 'Service 2', 'Email Support'],
                'excludes': ['Priority Support', 'Advanced Features'],
                'package_for': 'Students'
            },
            {
                'package_name': 'Premium Package',
                'includes': ['All Basic Features', 'Priority Support', 'Advanced Features', 'Consultation'],
                'excludes': [],
                'package_for': 'Professionals'
            },
            {
                'package_name': 'Enterprise Package',
                'includes': ['All Premium Features', 'Dedicated Support', 'Custom Solutions', 'Training'],
                'excludes': [],
                'package_for': 'Businesses'
            },
        ]
        for pkg_data in packages_data:
            Package.objects.get_or_create(package_name=pkg_data['package_name'], defaults=pkg_data)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(packages_data)} Package records'))

    def _seed_colleges(self):
        """Seed CollegesList model"""
        colleges_data = [
            {
                'college_name': 'MIT',
                'website_link': 'https://mit.edu',
                'state': 'Massachusetts',
                'public_private': 'private',
                'college_email': 'admissions@mit.edu'
            },
            {
                'college_name': 'Stanford University',
                'website_link': 'https://stanford.edu',
                'state': 'California',
                'public_private': 'private',
                'college_email': 'admissions@stanford.edu'
            },
            {
                'college_name': 'UC Berkeley',
                'website_link': 'https://berkeley.edu',
                'state': 'California',
                'public_private': 'public',
                'college_email': 'admissions@berkeley.edu'
            },
        ]
        for college_data in colleges_data:
            CollegesList.objects.get_or_create(college_name=college_data['college_name'], defaults=college_data)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(colleges_data)} CollegesList records'))

    def _seed_college_details(self):
        """Seed CollegeDetail model"""
        colleges = list(CollegesList.objects.all())
        if not colleges:
            return

        details = []
        for college in colleges:
            for i in range(3):
                details.append(CollegeDetail(
                    college=college,
                    college_name=college.college_name,
                    label=random.choice(['Facebook', 'Twitter', 'LinkedIn', 'Instagram', 'YouTube']),
                    link=f'https://{random.choice(["facebook", "twitter", "linkedin"])}.com/{college.college_name.lower()}'
                ))

        CollegeDetail.objects.bulk_create(details, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(details)} CollegeDetail records'))

    def _seed_persons(self):
        """Seed Person model"""
        first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
        
        persons = []
        for i in range(15):
            persons.append(Person(
                name=f'{random.choice(first_names)} {random.choice(last_names)}',
                email=f'person{i+1}@example.com',
                phone=f'+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}',
                dob=date(1990, 1, 1) + timedelta(days=random.randint(0, 10000)),
                address=f'{random.randint(1, 9999)} {random.choice(["Main", "Oak", "Elm", "Park"])} St, City {i+1}, ST {random.randint(10000, 99999)}'
            ))

        Person.objects.bulk_create(persons, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(persons)} Person records'))

    def _seed_part_timers(self):
        """Seed PartTimer model"""
        users = list(User.objects.all())
        if not users:
            return

        occupations = ['Student', 'Intern', 'Part-time Developer', 'Freelancer', 'Tutor']
        courses = ['Computer Science', 'Engineering', 'Business', 'Mathematics', None]
        years = ['1st Year', '2nd Year', '3rd Year', '4th Year', 'Graduate', None]

        part_timers = []
        for i in range(15):
            user = random.choice(users)
            part_timers.append(PartTimer(
                user=user.user_id,
                answered_questions=random.choice([True, False]),
                current_occupation=random.choice(occupations),
                year_of_study=random.choice(years) if i % 2 == 0 else None,
                course_name=random.choice(courses) if i % 2 == 0 else None,
                referred_by=random.choice(users).user_id if i % 3 == 0 else None
            ))

        PartTimer.objects.bulk_create(part_timers, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(part_timers)} PartTimer records'))

    def _seed_todos(self):
        """Seed Todo model"""
        # Note: Todo model requires Django User, not our custom User model
        # This will only work if Django auth users exist
        from django.contrib.auth.models import User as DjangoUser
        django_users = list(DjangoUser.objects.all())
        if not django_users:
            # Create a test user if none exists
            django_user, _ = DjangoUser.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
            django_user.set_password('testpass123')
            django_user.save()
            django_users = [django_user]

        todos = []
        tasks = ['Complete project', 'Review code', 'Write documentation', 'Fix bugs', 'Update dependencies',
                'Test features', 'Deploy application', 'Code review', 'Meeting preparation', 'Email follow-up']
        
        for i in range(15):
            todos.append(Todo(
                task=f'{random.choice(tasks)} {i+1}',
                completed=random.choice([True, False]),
                user=random.choice(django_users)
            ))

        Todo.objects.bulk_create(todos, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(todos)} Todo records'))

    def _seed_acs_parttimer_status(self):
        """Seed AcsParttimerStatus model"""
        users = list(User.objects.all())
        if not users:
            return

        statuses = []
        for i in range(20):
            user = random.choice(users)
            statuses.append(AcsParttimerStatus(
                parttimerName=user.full_name or f'PartTimer {i+1}',
                parttimerId=user.user_id,
                studentName=f'Student {i+1}',
                studentId=f'student_{i+1:03d}',
                date=timezone.now().date() - timedelta(days=random.randint(0, 30)),
                applicationsAppliedSearched=random.randint(0, 50),
                applicationsAppliedSaved=random.randint(0, 30),
                easyApply=random.randint(0, 20),
                recruiterDirectMessages=str(random.randint(0, 10)),
                connectMessages=str(random.randint(0, 15)),
                reason='Working on applications' if i % 3 == 0 else '',
                description=f'Status update for {timezone.now().date() - timedelta(days=random.randint(0, 30))}'
            ))

        AcsParttimerStatus.objects.bulk_create(statuses, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(statuses)} AcsParttimerStatus records'))

    def _seed_status_updates(self):
        """Seed StatusUpdates model"""
        users = list(User.objects.all())
        if not users:
            return

        subsidiaries = ['AMS', 'ACS', 'ASS', 'APS', 'ATI']
        sources = ['Web', 'Mobile', 'API', None]
        
        statuses = []
        for i in range(25):
            user = random.choice(users)
            status_date = timezone.now().date() - timedelta(days=random.randint(0, 60))
            
            statuses.append(StatusUpdates(
                user_id=user.user_id,
                user_name=user.full_name or f'User {i+1}',
                subsidary=random.choice(subsidiaries),
                source=random.choice(sources),
                date=status_date,
                description=f'Status update description for {status_date}' if i % 2 == 0 else None,
                studentName=f'Student {i+1}' if i % 3 == 0 else None,
                whatsappId=f'+1{random.randint(2000000000, 9999999999)}' if i % 4 == 0 else None,
                applicationsAppliedSearched=random.randint(0, 50) if i % 2 == 0 else 0,
                applicationsAppliedSaved=random.randint(0, 30) if i % 2 == 0 else 0,
                easyApply=random.randint(0, 20) if i % 2 == 0 else 0,
                recruiterDirectMessages=str(random.randint(0, 10)) if i % 3 == 0 else None,
                connectMessages=str(random.randint(0, 15)) if i % 3 == 0 else None,
                reason='Working on applications' if i % 4 == 0 else None,
                ticket_link=f'https://ticket-system.com/ticket/{i+1}' if i % 5 == 0 else None,
                github_link=f'https://github.com/user{i+1}/project' if i % 6 == 0 else None,
                account_name=f'Account {i+1}' if i % 7 == 0 else None,
                stock_name=f'STOCK{i+1}' if i % 8 == 0 else None,
                stock_quantity=random.randint(10, 1000) if i % 8 == 0 else None,
                stock_value=Decimal(f'{random.randint(10, 1000)}.{random.randint(10, 99)}') if i % 8 == 0 else None,
                transaction_type=random.choice(['buy', 'sell']) if i % 8 == 0 else None,
                total_current_amount=Decimal(f'{random.randint(1000, 50000)}.{random.randint(10, 99)}') if i % 9 == 0 else None,
                pickup_location=f'{random.randint(1, 999)} Main St, City {i+1}' if i % 10 == 0 else None,
                pickup_contact=f'{random.randint(200,999)}{random.randint(100,999)}{random.randint(1000,9999)}' if i % 10 == 0 else None,
                dropoff_location=f'{random.randint(1, 999)} Oak Ave, City {i+1}' if i % 10 == 0 else None,
                dropoff_contact=f'{random.randint(200,999)}{random.randint(100,999)}{random.randint(1000,9999)}' if i % 10 == 0 else None,
                distance_travelled=Decimal(f'{random.randint(1, 100)}.{random.randint(10, 99)}') if i % 10 == 0 else None,
                whatsapp_group_number=f'+1{random.randint(2000000000, 9999999999)}' if i % 11 == 0 else None,
                leave=random.choice([True, False]) if i % 10 == 0 else False
            ))

        StatusUpdates.objects.bulk_create(statuses, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(statuses)} StatusUpdates records'))

    def _seed_transactions(self):
        """Seed Transaction model"""
        subsidiaries = ['AMS', 'ACS', 'ASS', 'APS', 'ATI']
        transaction_types = ['credit', 'debit']
        payment_types = ['cash', 'upi', 'bank_transfer']
        currencies = ['USD', 'INR', 'EUR']
        
        names = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams', 'Charlie Brown']
        
        transactions = []
        for i in range(20):
            transaction_date = timezone.now() - timedelta(days=random.randint(0, 90))
            transactions.append(Transaction(
                receiver_name=random.choice(names),
                receiver_id=f'receiver_{i+1:03d}',
                sender_name=random.choice(names),
                sender_id=f'sender_{i+1:03d}',
                accountant_name=random.choice(names),
                accountant_id=f'accountant_{i+1:03d}',
                credited_amount=Decimal(f'{random.randint(100, 10000)}.{random.randint(10, 99)}'),
                debited_amount=Decimal(f'{random.randint(100, 10000)}.{random.randint(10, 99)}'),
                transaction_datetime=transaction_date,
                transaction_type=random.choice(transaction_types),
                payment_type=random.choice(payment_types),
                subsidiary=random.choice(subsidiaries),
                currency=random.choice(currencies),
                description=f'Transaction #{i+1}: Payment for services'
            ))

        Transaction.objects.bulk_create(transactions, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(transactions)} Transaction records'))

    def _seed_team_members(self):
        """Seed TeamMember model"""
        names = ['Alex Johnson', 'Sarah Chen', 'Michael Park', 'Emily Davis', 'James Wilson',
                'Lisa Anderson', 'David Brown', 'Jessica Taylor', 'Robert Martinez', 'Jennifer Lee']
        roles = ['Software Engineer', 'Project Manager', 'Designer', 'QA Engineer', 'DevOps Engineer',
                'Data Analyst', 'Product Manager', 'Business Analyst']
        subsidiaries = ['AMS', 'ACS', 'ASS', 'APS', 'ATI']
        
        members = []
        for i, name in enumerate(names):
            start_date = date(2020, 1, 1) + timedelta(days=random.randint(0, 1000))
            end_date = start_date + timedelta(days=random.randint(365, 1825)) if i % 3 != 0 else None
            selected_role = random.choice(roles)
            
            members.append(TeamMember(
                name=name,
                work_time_from=start_date,
                work_time_to=end_date or (timezone.now().date() + timedelta(days=365)),
                role=selected_role,
                description=f'{selected_role} with expertise in team collaboration and project management.',
                facebook_link=f'https://facebook.com/{name.lower().replace(" ", ".")}' if i % 2 == 0 else '',
                linkedin_link=f'https://linkedin.com/in/{name.lower().replace(" ", "-")}',
                github_link=f'https://github.com/{name.lower().replace(" ", "")}' if i % 3 == 0 else '',
                subsidiary=random.choice(subsidiaries)
            ))

        TeamMember.objects.bulk_create(members, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(members)} TeamMember records'))

    def _seed_device_allocations(self):
        """Seed DeviceAllocation model"""
        device_types = ['Laptop', 'Desktop', 'Tablet', 'Phone', 'Monitor', 'Keyboard', 'Mouse']
        device_names = ['MacBook Pro', 'Dell XPS', 'iPad Pro', 'iPhone 14', 'Samsung Monitor',
                       'Mechanical Keyboard', 'Wireless Mouse', 'Surface Pro', 'ThinkPad']
        users = list(User.objects.all())
        purposes = ['Development', 'Testing', 'General Use', 'Design Work', 'Video Editing', None]
        
        allocations = []
        for i in range(15):
            start_date = timezone.now().date() - timedelta(days=random.randint(0, 180))
            end_date = start_date + timedelta(days=random.randint(90, 365)) if i % 3 != 0 else (timezone.now().date() + timedelta(days=365))
            user = random.choice(users) if users else None
            
            allocations.append(DeviceAllocation(
                device_type=random.choice(device_types),
                device_name=random.choice(device_names),
                about_device=f'Device allocated for {random.choice(purposes) or "general use"}',
                allocated_to=user.full_name if user else f'User {i+1}',
                from_date=start_date,
                to_date=end_date,
                purpose=random.choice(purposes)
            ))

        DeviceAllocation.objects.bulk_create(allocations, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(allocations)} DeviceAllocation records'))

    def _seed_happiness_indexes(self):
        """Seed HappinessIndex model"""
        users = list(User.objects.all())
        if not users:
            return

        indexes = []
        for i in range(20):
            user = random.choice(users)
            index_date = timezone.now().date() - timedelta(days=random.randint(0, 30))
            
            # Check if already exists for this user and date
            if not HappinessIndex.objects.filter(employee=user, date=index_date).exists():
                indexes.append(HappinessIndex(
                    employee=user,
                    happiness_score=random.randint(1, 10),
                    description=f'Happiness index rating for {index_date}' if i % 2 == 0 else None,
                    date=index_date
                ))

        HappinessIndex.objects.bulk_create(indexes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(indexes)} HappinessIndex records'))

    def _seed_shopping_products(self):
        """Seed ShopingProduct model"""
        products_data = [
            {
                'name': 'Wireless Headphones',
                'link': 'https://example.com/products/headphones',
                'age_group': 'All Ages',
                'description': 'Premium wireless headphones with noise cancellation'
            },
            {
                'name': 'Smart Watch',
                'link': 'https://example.com/products/smartwatch',
                'age_group': 'Adults',
                'description': 'Feature-rich smartwatch with health tracking'
            },
            {
                'name': 'Laptop Stand',
                'link': 'https://example.com/products/laptop-stand',
                'age_group': 'Adults',
                'description': 'Ergonomic laptop stand for better posture'
            },
        ]
        # Note: ImageField requires actual files, so we skip image for now
        # You can add images manually or use a placeholder
        for product_data in products_data:
            ShopingProduct.objects.get_or_create(name=product_data['name'], defaults=product_data)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(products_data)} ShopingProduct records (images can be added manually)'))

