from datetime import date

class DateService:
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def get_weekday_info(self, year: int, month: int, day: int = 15) -> dict:
        """
        Returns weekday number and name.
        """
        current_date = date(year, month, day)
        weekday_num = current_date.weekday()
        
        return {
            "weekday_number": weekday_num,
            "weekday_name": self.DAYS[weekday_num]
        }


    # Update arguments to accept target_weekday and target_day
    def count_matching_dates(self, start_date: date, end_date: date, target_weekday: int, target_day: int) -> dict:
        matches = []
        
        # Start logic
        start_year = start_date.year
        start_month = start_date.month
        
        # If the start date is past the target day in the current month, skip to next month
        if start_date.day > target_day:
            if start_month == 12:
                start_year += 1
                start_month = 1
            else:
                start_month += 1
        
        current_year = start_year
        current_month = start_month
        
        while True:
            try:
                # Try to create date for the specific target day (e.g., the 13th)
                check_date = date(current_year, current_month, target_day)
            except ValueError:
                # This handles cases like "February 30th" -> Skip this month
                # Move to next month logic below
                pass
            else:
                # If date is valid, check bounds and weekday
                if check_date > end_date:
                    break
                
                # Check weekday matches (0=Mon, 6=Sun)
                if check_date.weekday() == target_weekday:
                    matches.append(check_date)
            
            # Move to next month
            if current_month == 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1
        
        return {
            "count": len(matches),
            "dates": matches
        }

# Create a singleton instance to be imported
date_service = DateService()